from flask import Blueprint, render_template, redirect, url_for, flash
from website.forms import LoginForm, RegistrationForm, SecureNoteForm, ChangeAccountInformationForm
# from website.models import User

auth = Blueprint("auth",
                  __name__,
                  static_folder="static",
                  template_folder="templates/auth")


""" This file handles all functions for User account information and routing
It controls what the user views when logged in , and handles when they are not
logged in."""

@auth.route('/dashboard', defaults={'username': 'izzy'})
@auth.route('/user/<username>/')
def dashboard(username):
   #  user = User.query.filter_by(name=username).first()
   if username:
      return render_template('dashboard.html')

   flash('Sign in to view your dashboard.')
   return redirect(url_for('auth.login'))

@auth.route("/login", methods=["GET","POST"])
def login():
   form = LoginForm()
   return render_template("user_login.html", form=form)

@auth.route("/register", methods=["GET","POST"])
def register():
   form = RegistrationForm()
   return render_template('register.html', form=form)

@auth.route("/account", methods=["GET","POST"])
def account():
   form = ChangeAccountInformationForm()
   return render_template('account.html')

@auth.route("/settings")
def settings():
   return render_template('settings.html')


# Features of the Password Manager
# User logins
@auth.route('/logins')
def show_logins():
   return render_template('logins.html')

# User Secure Notes
@auth.route('/notes')
def notes():
   form = SecureNoteForm()
   return render_template('notes.html', form=form)
