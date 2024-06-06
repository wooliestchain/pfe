import sqlalchemy
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import pandas as pd
import dash
from dash import dcc, html, Input, Output
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import bcrypt
import folium
from infojson import extract
import json
from collections import defaultdict
import datetime
import map
import plotly.express as px

#Charger le fichier global.json
def load_data():
    with open('global.json', 'r', encoding='utf-8') as f:
        return json.load(f)


app = Flask('__name__')
app.secret_key = 'your-secret-key'

#Connexion à la base de données
conn = mysql.connector.connect(
    host="localhost",
    database="pfe",
    user="root",
    password=""
)
cur = conn.cursor()
#SQL CONNECTION
def dash_menu():
    # Charger les données
    df = pd.read_csv('dab_net.csv')
    df['month'] = pd.Categorical(df['month'], categories=[
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'], ordered=True)

    # Créer une instance de Dash
    dash_app = dash.Dash(__name__, server=app, url_base_pathname='/dashboard/')

    # Initialiser le graphique à anneaux avec la répartition des types de cartes pour l'ensemble du dataset
    initial_card_type_counts = df['card_type'].value_counts()
    initial_donut_figure = {
        'data': [
            {
                'labels': initial_card_type_counts.index,
                'values': initial_card_type_counts.values,
                'type': 'pie',
                'hole': .10
            }
        ],
        'layout': {
            'title': 'Card Type Distribution (All Data)',
            'height': 400
        }
    }

    # Configurer le layout de Dash
    dash_app.layout = html.Div([
        dcc.Dropdown(
            id='month-dropdown',
            options=[{'label': month, 'value': month} for month in df['month'].cat.categories],
            value=df['month'].cat.categories[0]
        ),
        dcc.Dropdown(
            id='currency-dropdown',
            options=[{'label': currency, 'value': currency} for currency in df['currency'].unique()],
            multi=True
        ),
        dcc.Dropdown(
            id='weather-dropdown',
            options=[{'label': weather, 'value': weather} for weather in df['weather_main'].unique()],
            multi=True
        ),
        dcc.Dropdown(
            id='message-dropdown',
            options=[{'label': message, 'value': message} for message in df['message_text'].unique()],
            multi=True
        ),
        html.Div(id='total-transactions', style={'margin-top': 20, 'font-size': '20px'}),  # Element pour afficher le nombre total de transactions
        html.Div([
            html.Div([
                dcc.Graph(id='transaction-area-graph', className='graph')
            ], className="col-md-6"),
            html.Div([
                dcc.Graph(id='card-type-donut', figure=initial_donut_figure, className='graph'),
                dcc.Graph(id='weekday-treemap', className='graph')
            ], className="col-md-6"),
        ], className="row"),
        html.Div([
            html.Div([
                dcc.Graph(id='transaction-map', className='graph')
            ], className="col-md-12")
        ], className="row")
    ])

    # Callback pour mettre à jour les graphiques
    @dash_app.callback(
        [Output('transaction-area-graph', 'figure'),
         Output('card-type-donut', 'figure'),
         Output('total-transactions', 'children'),
         Output('weekday-treemap', 'figure'),
         Output('transaction-map', 'figure')],  # Ajout de l'élément pour la carte
        [Input('currency-dropdown', 'value'),
         Input('weather-dropdown', 'value'),
         Input('message-dropdown', 'value')]
    )
    def update_graphs(selected_currencies, selected_weathers, selected_messages):
        filtered_df = df.copy()  # Copie du DataFrame d'origine

        if selected_currencies:
            filtered_df = filtered_df[filtered_df['currency'].isin(selected_currencies)]
        if selected_weathers:
            filtered_df = filtered_df[filtered_df['weather_main'].isin(selected_weathers)]
        if selected_messages:
            filtered_df = filtered_df[filtered_df['message_text'].isin(selected_messages)]

        card_type_counts = filtered_df['card_type'].value_counts()
        donut_figure = {
            'data': [
                {
                    'labels': card_type_counts.index,
                    'values': card_type_counts.values,
                    'type': 'pie',
                    'hole': .4
                }
            ],
            'layout': {
                'title': 'Card Type Distribution',
                'height': 400
            }
        }

        transactions_per_month = filtered_df.groupby('month').size().reindex(df['month'].cat.categories)
        area_figure = {
            'data': [
                {
                    'x': transactions_per_month.index,
                    'y': transactions_per_month.values,
                    'type': 'scatter',
                    'mode': 'lines',
                    'fill': 'tozeroy'
                }
            ],
            'layout': { 'title': 'Monthly Transactions'
            }
        }

        # Treemap pour afficher le nombre de transactions par jour de la semaine (weekday)
        transactions_per_weekday = filtered_df['weekday'].value_counts().reset_index()
        transactions_per_weekday.columns = ['weekday', 'count']
        weekday_treemap = px.treemap(transactions_per_weekday, path=['weekday'], values='count', title='Transactions per Weekday')
        weekday_treemap.update_layout(width=600, height=400, margin=dict(l=20, r=20, t=40, b=20))  # Ajustements de la taille et des marges

        # Carte pour afficher les transactions par emplacement ATM
        atm_transactions = filtered_df.groupby(['atm_lat', 'atm_lon']).size().reset_index(name='count')
        transaction_map = px.scatter_mapbox(atm_transactions, lat='atm_lat', lon='atm_lon', size='count',
                                            color='count', size_max=30, zoom=3)
        transaction_map.update_layout(mapbox_style="open-street-map", title='Transactions by ATM Location')

        total_transactions = len(filtered_df)  # Nombre total de transactions
        return area_figure, donut_figure, f'Total Transactions: {total_transactions}', weekday_treemap, transaction_map

dash_menu()

#Page Home
@app.route('/')
def home():
    if 'email' in session:
        user_role = session.get('role', None)  # Récupérer le rôle de l'utilisateur depuis la session
        return render_template('home.html', email=session['email'], role=user_role)
    else:
        return render_template('home.html')

#Page Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # On récupère les informations rentrées dans le formulaire
        email = request.form['email']
        pwd = request.form['password']

        # Requête pour vérifier l'email et le mot de passe, ainsi que l'existence d'un jeton valide
        query = """
        SELECT user_id, email, password, role, jeton
        FROM users
        WHERE email = %s
        """
        cur.execute(query, (email,))
        user = cur.fetchone()

        # Si l'utilisateur existe et que le mot de passe est correct
        if user and bcrypt.checkpw(pwd.encode('utf-8'), user[2].encode('utf-8')):
            session['email'] = user[1]
            session['role'] = user[3]

            # Insertion dans la table log
            log_query = """
                        INSERT INTO log_entry (email, date, time)
                        VALUES (%s, %s, %s)
                        """
            current_date = datetime.datetime.now().date()
            current_time = datetime.datetime.now().time()
            cur.execute(log_query, (user[1], current_date, current_time))
            conn.commit()

            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid username or password or no valid token')

    return render_template('login.html')


#Route pour s'inscrire
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        nom = request.form['nom']
        prenom = request.form['prenom']
        role = request.form['role']
        pwd = request.form['password']

        # Vérifiez si l'email existe déjà
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        if user:
            # Si l'email existe déjà, retournez un message d'erreur
            error = "L'email existe déjà. Veuillez utiliser un autre email."
            return render_template('register.html', error=error)

        # Si l'email n'existe pas, continuez avec l'inscription
        hashed_pwd = bcrypt.hashpw(pwd.encode('utf-8'), bcrypt.gensalt())
        cur.execute("""INSERT INTO users (email, nom, prenom, role, password) VALUES (%s, %s, %s, %s, %s);""",
                    (email, nom, prenom, role, hashed_pwd))
        conn.commit()
        return redirect(url_for('login'))
    return render_template('register.html')


# @app.route("/map")
# def base():
#     map = folium.Map(
#         location=[10.54484, 12.6565]
#     )
#     map_html = map._repr_html_()
#     return render_template('home.html', map_html=map_html)

#Route pour afficher la carte et marquer chaque point
@app.route('/map')
def dab():
    if 'email' in session:
        data = load_data()

        # Initialiser la carte
        map = folium.Map(location=[36.86461188050044, 10.217478287058501], zoom_start=12)

        # Ajouter des marqueurs pour chaque point
        for point in data:
            folium.Marker(
                location=[point['latitude'], point['longitude']],
                popup=f"{point['secteur']}, {point['ville']}",
                tooltip=f"Densité: {point['densite_100_metter']}, DAB Near: {point['dab_near']}"
            ).add_to(map)

        # Convertir la carte en HTML
        map_html = map._repr_html_()

        # Compter le nombre de DAB par ville
        dab_count_by_city = defaultdict(int)
        for point in data:
            dab_count_by_city[point['ville']] += 1

        return render_template('carte.html', map_html=map_html, dab_count_by_city=dab_count_by_city, email = session['email'])
    else:
        return redirect(url_for('login'))  # Rediriger vers la page de connexion si l'utilisateur n'est pas connecté


@app.route('/city/<ville>')
def city(ville):
    if 'email' in session:
        data = load_data()
        city_data = [point for point in data if point['ville'].lower() == ville.lower()]

        page = request.args.get('page', 1, type=int)
        per_page = 10
        total = len(city_data)
        start = (page - 1) * per_page
        end = start + per_page
        paginated_data = city_data[start:end]

        map = folium.Map(location=[city_data[0]['latitude'], city_data[0]['longitude']], zoom_start=12)
        for point in paginated_data:
            folium.Marker(
                location=[point['latitude'], point['longitude']],
                popup=f"{point['secteur']}, {point['ville']}",
                tooltip=f"Densité: {point['densite_100_metter']}, DAB Near: {point['dab_near']}"
            ).add_to(map)

        map_html = map._repr_html_()

        return render_template('city.html', map_html=map_html, ville=ville, city_data=paginated_data, page=page, total=total, per_page=per_page, email = session['email'])
    else:
        return redirect(url_for('login'))  # Rediriger vers la page de connexion si l'utilisateur n'est pas connecté

def save_data(data):
    with open('global.json', 'w') as file:
        json.dump(data, file, indent=4)

@app.route('/dab/<int:dab_index>', methods=['GET', 'POST'])
def dab_details(dab_index):
    if 'email' in session:
        data = load_data()
        dab_data = next((item for item in data if item["dab_index"] == dab_index), None)
        if not dab_data:
            return "DAB not found", 404

        if request.method == 'POST' and 'delete' in request.form:
            if session.get('role') == 'Décideur':
                data.remove(dab_data)
                # Mettre à jour les indices des autres DABs
                for index, dab in enumerate(data):
                    dab['dab_index'] = index + 1

                # Sauvegarder les modifications dans le fichier JSON
                with open('global.json', 'w') as file:
                    json.dump(data, file, indent=4)

                return redirect(url_for('home'))

        # Créer une carte avec un marqueur pour le DAB sélectionné
        map = folium.Map(location=[dab_data['latitude'], dab_data['longitude']], zoom_start=15)
        folium.Marker(
            location=[dab_data['latitude'], dab_data['longitude']],
            popup=f"{dab_data['secteur']}, {dab_data['ville']}",
            tooltip=f"Densité: {dab_data['densite_100_metter']}, DAB Near: {dab_data['dab_near']}"
        ).add_to(map)
        map_html = map._repr_html_()

        return render_template('dab.html', gab_data=dab_data, map_html=map_html, email=session['email'], role=session.get('role'))
    else:
        return redirect(url_for('login'))  # Rediriger vers la page de connexion si l'utilisateur n'est pas connecté


@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))

@app.route('/ajouter', methods=['GET', 'POST'])
def ajouter():
    if 'email' in session or session.get('role') == 'Décideur' or session.get('role') == 'Admin':
        if request.method == 'POST':
            # Récupération des données du formulaire
            secteur = request.form['secteur']
            longitude = float(request.form['longitude'])
            latitude = float(request.form['latitude'])
            densite = float(request.form['densite_100_metter'])
            ville = request.form['ville']
            dab_near = float(request.form['dab_near'])
            magasins = []
            for i in range(len(request.form.getlist('magasin_nom'))):
                magasin = {
                    'nom': request.form.getlist('magasin_nom')[i],
                    'distance': float(request.form.getlist('magasin_distance')[i])
                }
                magasins.append(magasin)

            # Calcul de l'efficacité et de la distance moyenne aux magasins
            weight_density = 0.5  # poids fictif, ajustez selon vos besoins
            weight_dab_near = 0.5  # poids fictif, ajustez selon vos besoins
            efficacite = (weight_density * densite) + (weight_dab_near * dab_near)
            distance_mean = sum(m['distance'] for m in magasins) / len(magasins)

            # Charger les dabs existants depuis le fichier JSON
            try:
                with open('final.json', 'r') as file:
                    dabs = json.load(file)
            except FileNotFoundError:
                dabs = []

            # Déterminer le nouvel index du dab
            dab_index = dabs[-1]['dab_index'] + 1 if dabs else 1

            # Créer le nouveau dab
            new_dab = {
                "dab_index": dab_index,
                "longitude": longitude,
                "latitude": latitude,
                "densite_100_metter": densite,
                "secteur": secteur,
                "ville": ville,
                "dab_near": dab_near,
                "magasin": magasins,
                "efficacite": efficacite,
                "distance_mean": distance_mean
            }

            # Sauvegarder le nouveau dab dans le fichier JSON
            dabs.append(new_dab)
            with open('final.json', 'w') as file:
                json.dump(dabs, file, indent=4)

            # Rediriger vers la page de validation
            return redirect(url_for('valider', dab_index=dab_index))

        return render_template('ajouter.html')
    else:
        return redirect(url_for('home'))

@app.route('/valider/<int:dab_index>', methods=['GET', 'POST'])
def valider(dab_index):
    if 'email' in session and session.get('role') == 'Décideur':
        # Charger les dabs existants depuis le fichier JSON
        with open('final.json', 'r') as file:
            dabs = json.load(file)

        # Trouver le dab correspondant
        dab = next((d for d in dabs if d['dab_index'] == dab_index), None)

        if not dab:
            return redirect(url_for('ajouter'))

        if request.method == 'POST':
            # Si l'utilisateur valide les informations
            if request.form.get('action') == 'Valider':
                return redirect(url_for('home'))
            # Si l'utilisateur veut modifier les informations
            elif request.form.get('action') == 'Modifier':
                return redirect(url_for('ajouter'))

        # Créer la carte avec folium
        import folium
        from folium.plugins import MarkerCluster

        m = folium.Map(location=[dab['latitude'], dab['longitude']], zoom_start=15)
        folium.Marker(
            location=[dab['latitude'], dab['longitude']],
            popup=f"DAB {dab['dab_index']}",
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(m)

        # Sauvegarder la carte en HTML
        m.save('templates/map.html')

        return render_template('valid.html', dab=dab)
    else:
        return redirect(url_for('home'))






@app.route('/admin',  methods=['GET', 'POST'])
def admin():
    if 'email' in session and session.get('role') == 'Admin':

        query = "SELECT user_id, email, nom, prenom, role FROM users"
        cur.execute(query)
        users = cur.fetchone()

        page = request.args.get('page', 1, type=int)
        per_page = 10
        total = len(users)
        start = (page - 1) * per_page
        end = start + per_page
        paginated_data = users[start:end]

        return render_template('admin.html', page=page, total=total, per_page=per_page, paginated_data=paginated_data)
    else:
        return redirect(url_for('home'))



if __name__ == '__main__':
    app.run(debug=True)
