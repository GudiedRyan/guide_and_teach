from flask import render_template, Blueprint

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
@main.route('/HOME')
def home():
    return render_template('about.html', title='About Page')
