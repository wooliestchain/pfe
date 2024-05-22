import sqlalchemy
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import bcrypt
import folium


app = Flask('__name__')
app.secret_key = 'your-secret-key'

conn = mysql.connector.connect(
    host="localhost",
    database="pfe",
    user="root",
    password=""
)
cur = conn.cursor()
#SQL CONNECTION

@app.route('/')
def home():
    if 'email' in session:
        return render_template('home.html', email = session['email'])
    else:
        return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        pwd = request.form['password']
        cur.execute(f"select email, password from users where email = '{email}'")
        user = cur.fetchone()
        if user and bcrypt.checkpw(pwd.encode('utf-8'), user[1].encode('utf-8')):
            session['email'] = user[0]
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

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

@app.route("/map")
def base():
    map = folium.Map(
        location=[10.54484, 12.6565]
    )
    map_html = map._repr_html_()
    return render_template('home.html', map_html=map_html)


if __name__ == '__main__':
    app.run(debug=True)