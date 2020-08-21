import secrets
from flask import render_template, url_for, flash, redirect
from guide_and_teach import app, db, bcrypt
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
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created! You can now log in.')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('home'))
    return render_template('login.html', title='Login', form=form)