import os
from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'd5f40df13ec35735ece1cf7ec34e408d'

from guide_and_teach import routes