from flask import render_template, url_for, flash, redirect
from website import app
from website.forms import RegistrationForm


@app.route('/')
@app.route('/home')
def index():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Signed Up Successfully!', category='success')
    return render_template('auth/register.html', title='Registration', form=form)