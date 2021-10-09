import os
from importlib import metadata

from flask import Flask
from flask_login import LoginManager, current_user
from flask_principal import Principal, identity_loaded, UserNeed, RoleNeed

from .account import account as account_blueprint
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

    Principal(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        # Set the identity user object
        identity.user = current_user

        # Add the UserNeed to the identity
        if hasattr(current_user, 'id'):
            identity.provides.add(UserNeed(current_user.id))

        # Add the 'admin' RoleNeed to the identity
        if hasattr(current_user, 'isop'):
            identity.provides.add(RoleNeed('admin'))

    app.jinja_env.filters['format_currency'] = format_currency

    @app.context_processor
    def get_version():
        if app.env == 'production':
            version = metadata.version('nanposweb')
        else:
            version = 'devel'
        return dict(version=version)

    # blueprint for auth routes in our app
    app.register_blueprint(auth_blueprint)

    # blueprint for main parts of app
    app.register_blueprint(main_blueprint)

    # blueprint for account management
    app.register_blueprint(account_blueprint)

    # blueprint for admin parts of app
    app.register_blueprint(admin_blueprint)

    return app


app = create_app()
