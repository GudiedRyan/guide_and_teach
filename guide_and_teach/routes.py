from flask import render_template, url_for, flash, redirect
from guide_and_teach import app, db
from guide_and_teach.forms import RegistrationForm, LoginForm
from guide_and_teach.models import User, Course

@app.route('/')
@app.route('/home')
def home():
    return render_template('about.html', title='About Page')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash("Success!")
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('home'))
    return render_template('login.html', title='Login', form=form)