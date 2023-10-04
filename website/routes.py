from flask import render_template, url_for, flash, redirect
from website import app


@app.route('/')
@app.route('/dashboard')
def dashboard():
    return render_template('auth/dashboard.html')

@app.route('/logins')
def show_logins():
    return render_template('logins.html')