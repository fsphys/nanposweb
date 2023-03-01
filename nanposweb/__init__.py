import os
from importlib import metadata

from flask import Flask, flash, session, redirect, url_for
from flask_login import LoginManager, current_user
from flask_principal import Principal, identity_loaded, UserNeed, RoleNeed

from .account import account_bp
from .admin import admin_bp
from .auth import auth_bp, card_auth_bp
from .db import db
from .db.models import User
from .helpers import format_currency
from .main import main_bp


def create_app(test_config=None):
    # create and configure the nanposweb_app
    nanposweb_app = Flask(__name__, instance_relative_config=True)
    nanposweb_app.config.from_mapping(
        SECRET_KEY='dev',
        SESSION_COOKIE_SECURE=True,
        REMEMBER_COOKIE_SECURE=True,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_DATABASE_URI='postgresql://nanpos:nanpos@localhost:5432/nanpos',
        TERMINAL_LOGOUT_TIMEOUT=30,  # logout timeout for Terminal mode in seconds, set to none to disable
        QUICK_CANCEL_SEC=60,  # Second-Limit for canceling a revenue
        BANK_DATA=None,
        FAVORITES_DISPLAY=3,  # Amount of favorite products which should get highlighted
        FAVORITES_DAYS=100,  # Timespan for calculation of favorite products in Days
        ALLOW_SIGNUP=False,  # Disable user sign up
        ENABLE_CARD_READER=False,  # Disable the card reader by default
    )
    if nanposweb_app.env != 'production':
        nanposweb_app.config.from_mapping(
            SESSION_COOKIE_SECURE=False,
            REMEMBER_COOKIE_SECURE=False,
        )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        nanposweb_app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        nanposweb_app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(nanposweb_app.instance_path)
    except OSError:
        pass

    db.init_app(nanposweb_app)

    Principal(nanposweb_app)

    login_manager = LoginManager()
    login_manager.login_message_category = 'info'
    login_manager.init_app(nanposweb_app)

    @login_manager.unauthorized_handler
    def unauthorized():
        if login_manager.localize_callback is not None:
            flash(login_manager.localize_callback(login_manager.login_message),
                  category=login_manager.login_message_category)
        else:
            flash(login_manager.login_message, category=login_manager.login_message_category)

        if session.get('terminal', False):
            return redirect(url_for('auth.login', terminal=True))
        else:
            return redirect(url_for('auth.login'))

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @identity_loaded.connect_via(nanposweb_app)
    def on_identity_loaded(sender, identity):
        # Set the identity user object
        identity.user = current_user

        # Add the UserNeed to the identity
        if hasattr(current_user, 'id'):
            identity.provides.add(UserNeed(current_user.id))

        # Add the 'admin' RoleNeed to the identity
        if hasattr(current_user, 'isop'):
            identity.provides.add(RoleNeed('admin'))

    nanposweb_app.jinja_env.filters['format_currency'] = format_currency

    @nanposweb_app.context_processor
    def get_version():
        if nanposweb_app.debug:
            version = 'devel'
        else:
            version = metadata.version('nanposweb')
        return dict(version=version)

    @nanposweb_app.context_processor
    def get_utils():
        utils = []
        if nanposweb_app.config.get('BANK_DATA', False):
            utils.append(('main.bank_account', 'Bank Account'))
        if nanposweb_app.config.get('utils', False):
            utils.extend(nanposweb_app.config['utils'])
        return dict(utils=utils)

    # blueprint for auth routes in our nanposweb_app
    nanposweb_app.register_blueprint(auth_bp)

    # blueprint for card auth route in nanposweb
    if nanposweb_app.config.get('ENABLE_CARD_READER', False):
        nanposweb_app.register_blueprint(card_auth_bp)

    # blueprint for main parts of nanposweb_app
    nanposweb_app.register_blueprint(main_bp)

    # blueprint for account management
    nanposweb_app.register_blueprint(account_bp)

    # blueprint for admin parts of nanposweb_app
    nanposweb_app.register_blueprint(admin_bp)

    return nanposweb_app


app = create_app()
