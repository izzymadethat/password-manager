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

@auth.route('/dashboard')
@auth.route('/user/<username>/')
def dashboard():
   #  user = User.query.filter_by(name=username).first()
   return render_template('dashboard.html')

@auth.route("/login", methods=["GET","POST"])
def login():
   form = LoginForm()
   return render_template("user_login.html", form=form)

@auth.route("/register", methods=["GET","POST"])
def register():
   form = RegistrationForm()
   if form.validate_on_submit():
      flash(f'Welcome {form.name.data.capitalize()}! You may now login.', category='success')
      return redirect(url_for('auth.dashboard'))
   # elif form.confirmation_email != form.email:
   #    flash(f"Emails do not match!", category='danger')
   return render_template('register.html', form=form, name=form.name.data)

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
