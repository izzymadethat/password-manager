from flask_wtf import FlaskForm
from wtforms import (StringField, EmailField,
                     PasswordField, BooleanField,
                     TextAreaField, IntegerField,
                     DateField, SubmitField)
from wtforms.widgets import PasswordInput
from wtforms.validators import DataRequired, Length, EqualTo

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), Length(min=6, max=16)])
    email = EmailField('Email', validators=[DataRequired()])
    confirmation_email = EmailField('Confirm Email', validators=[DataRequired(), EqualTo('email')])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=8, max=20)])
    confirmation_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class AddLoginForm(FlaskForm):
    title = StringField('Title')
    website = StringField('Title', validators=[DataRequired()])
    username = StringField('Username or Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    notes = TextAreaField('Notes/Description')
    favorite = BooleanField('Save as favorite?')
    submit = SubmitField('Add Login Information')

class SecureNoteForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    note = TextAreaField('', validators=[DataRequired()])
    submit = SubmitField('Add Secure Note')

class CreditCardForm(FlaskForm):
    name = StringField('Name of Card', validators=[DataRequired()])
    cc_number = IntegerField('Credit Card Number', validators=[DataRequired()])
    exp_date = DateField('Expires', validators=[DataRequired()])
    cvv_code = IntegerField('Security Code (Optional)')
    zip_code = IntegerField('Zip Code', validators=[DataRequired()])
    default = BooleanField('Primary Card')
    submit = SubmitField('Add Credit Card to Wallet')

class PasswordTextInput(PasswordInput):
    input_type = "text"

class ChangeAccountInformationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20)])
