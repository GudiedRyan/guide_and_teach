from flask import render_template, url_for
from guide_and_teach import app
from guide_and_teach.forms import RegistrationForm, LoginForm


@app.route('/')
def home():
    return render_template('about.html', title='About Page')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    return render_template('register.html', title='register', form=form)