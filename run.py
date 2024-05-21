from flask import Flask, render_template, request, redirect, url_for, session

def home():
    if 'username' in session:
        return render_template('home.html', username = session['username'])
    else:
        return render_template('home.html')