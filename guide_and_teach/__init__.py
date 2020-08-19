import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = ''
app.config['SQLALCHEMY_DATEBASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

from guide_and_teach import routes