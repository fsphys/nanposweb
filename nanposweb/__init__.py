import os

from flask import Flask
from flask_login import LoginManager

from .admin import admin as admin_blueprint
from .auth import auth as auth_blueprint
from .db import db
from .main import main as main_blueprint
from .models import User
from .util import format_currency


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SESSION_COOKIE_SECURE=True,
        REMEMBER_COOKIE_SECURE=True,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_DATABASE_URI='postgresql://nanpos:nanpos@localhost:5432/nanpos',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    app.jinja_env.filters['format_currency'] = format_currency

    # blueprint for auth routes in our app
    app.register_blueprint(auth_blueprint)

    # blueprint for main parts of app
    app.register_blueprint(main_blueprint)

    # blueprint for admin parts of app
    app.register_blueprint(admin_blueprint)

    return app


app = create_app()

