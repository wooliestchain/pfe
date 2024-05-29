import sqlalchemy
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import bcrypt
import folium
from infojson import extract
import json
from collections import defaultdict
import datetime
import map
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

#Page Home
@app.route('/')
def home():
    if 'email' in session:
        return render_template('home.html', email = session['email'])
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
        SELECT u.user_id, u.email, u.password
        FROM users u
        JOIN token t ON u.user_id = t.user_id
        WHERE u.email = %s AND t.token_id IS NOT NULL
        """
        cur.execute(query, (email,))
        user = cur.fetchone()

        # Si l'utilisateur existe et que le mot de passe est correct
        if user and bcrypt.checkpw(pwd.encode('utf-8'), user[2].encode('utf-8')):
            session['email'] = user[1]

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
        hashed_pwd = bcrypt.hashpw(pwd.encode('utf-8'), bcrypt.gensalt())
        cur.execute(""" INSERT INTO users (email, nom, prenom, role, password) VALUES (%s, %s, %s, %s, %s);""", (email, nom, prenom, role,  hashed_pwd))
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

    return render_template('carte.html', map_html=map_html, dab_count_by_city=dab_count_by_city)


@app.route('/city/<ville>')
def city(ville):
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

    return render_template('city.html', map_html=map_html, ville=ville, city_data=paginated_data, page=page, total=total, per_page=per_page)

@app.route('/dab/<int:dab_index>')
def dab_details(dab_index):
    data = load_data()
    dab_data = next((item for item in data if item["dab_index"] == dab_index), None)
    if not dab_data:
        return "DAB not found", 404

    # Créer une carte avec un marqueur pour le DAB sélectionné
    map = folium.Map(location=[dab_data['latitude'], dab_data['longitude']], zoom_start=15)
    folium.Marker(
        location=[dab_data['latitude'], dab_data['longitude']],
        popup=f"{dab_data['secteur']}, {dab_data['ville']}",
        tooltip=f"Densité: {dab_data['densite_100_metter']}, DAB Near: {dab_data['dab_near']}"
    ).add_to(map)
    map_html = map._repr_html_()

    return render_template('dab.html', gab_data=dab_data, map_html=map_html)

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))




if __name__ == '__main__':
    app.run(debug=True)