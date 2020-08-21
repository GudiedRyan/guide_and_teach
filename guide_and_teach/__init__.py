import os
import secrets
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

generated_key = secrets.token_urlsafe(20)
app = Flask(__name__)
app.config['SECRET_KEY'] = generated_key
app.config['SQLALCHEMY_DATEBASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from guide_and_teach import routes