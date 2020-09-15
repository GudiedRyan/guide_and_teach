from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from guide_and_teach.config import Config


db = SQLAlchemy()
migrate = Migrate(db)
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    from guide_and_teach.users.routes import users
    from guide_and_teach.courses.routes import courses
    from guide_and_teach.students.routes import students
    from guide_and_teach.grades.routes import grades
    from guide_and_teach.main.routes import main
    app.register_blueprint(users)
    app.register_blueprint(courses)
    app.register_blueprint(students)
    app.register_blueprint(grades)
    app.register_blueprint(main)

    return app