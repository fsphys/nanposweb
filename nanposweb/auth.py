from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, session
from flask_login import login_required, logout_user, login_user, current_user
from flask_principal import identity_changed, Identity, AnonymousIdentity

from .db.models import User
from .db import db
from .forms import LoginForm, SignUpForm, CardLoginForm
from .helpers import check_hash, calc_hash

auth_bp = Blueprint('auth', __name__)
card_auth_bp = Blueprint('card', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('Already logged in.')
        return redirect(request.args.get('next') or url_for('main.index'))

    allow_sign_up = current_app.config.get("ALLOW_SIGNUP", False)

    session['terminal'] = request.args.get('terminal', False, type=bool)
    form = LoginForm()
    form2 = CardLoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(name=form.username.data).one_or_none()

            if user and check_hash(user.pin, form.pin.data):
                login_user(user, remember=form.remember.data)
                flash('Logged in', category='success')

                identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))

                return redirect(request.args.get('next') or url_for('main.index'))
            else:
                flash('Please check your login details and try again.', category='danger')
        else:
            flash('Submitted form was not valid!', category='danger')

    return render_template('login.html', form=form, form2=form2, allow_sign_up=allow_sign_up)


@card_auth_bp.route('/card_login', methods=['POST'])
def card_login():
    if current_user.is_authenticated:
        flash('Already logged in.')
        return redirect(request.args.get('next') or url_for('main.index'))

    session['terminal'] = request.args.get('terminal', False, type=bool)

    form = CardLoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            # Check if card reader checks are enabled
            if current_app.config.get("ENABLE_CARD_READER", False) and current_app.config.get("VERIFY_CARD_READER", False):
                # Try verifying the card reader
                if form.reader.data not in current_app.config.get("VERIFIED_CARD_READERS", []):
                    # Redirect back to the login page
                    if session.get('terminal', False):
                        return redirect(url_for('auth.login', terminal=True))
                    else:
                        return redirect(url_for('auth.login'))

            user = User.query.filter_by(card=calc_hash(form.card.data)).one_or_none()

            if user:
                login_user(user, remember=False)

                identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))

                return redirect(request.args.get('next') or url_for('main.index'))
            else:
                flash('Please check your login details and try again.', category='danger')
                return redirect(url_for('auth.login'))
        else:
            flash('Submitted form was not valid!', category='danger')
            if session.get('terminal', False):
                return redirect(url_for('auth.login', terminal=True))
            else:
                return redirect(url_for('auth.login'))
    # Default redirect
    if session.get('terminal', False):
        return redirect(url_for('auth.login', terminal=True))
    else:
        return redirect(url_for('auth.login'))


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()

    # Remove session keys set by Flask-Principal
    for key in ('identity.id', 'identity.auth_type'):
        session.pop(key, None)

    session.pop('impersonate', None)  # remove impersonation status to avoid weird behaviours

    # Tell Flask-Principal the user is anonymous
    identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())
    flash('Logged out')

    if session.get('terminal', False):
        return redirect(url_for('auth.login', terminal=True))
    else:
        return redirect(url_for('auth.login'))


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():

    # If there is a current user, and he is already logged in then redirect him to the main ui
    if current_user.is_authenticated:
        flash('Already logged in.')
        return redirect(request.args.get('next') or url_for('main.index'))

    # Redirect to the login page if sign up is disabled
    if current_app.config.get("ALLOW_SIGNUP", False) is False:
        return redirect(url_for('auth.login'))

    # Ensure proper terminal support for the page
    session['terminal'] = request.args.get('terminal', False, type=bool)

    # Create an instance for the signup form
    form = SignUpForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            # Check if there is a user with the username
            check_user = User.query.filter_by(name=form.username.data).one_or_none()

            if form.pin.data != form.repeat_pin.data:
                flash('PIN isn\'t matching. Please reenter it.', category='danger')
            elif check_user is not None:
                flash('Username already taken! Please choose a different one.', category='danger')
            else:
                # Register the user
                user = User(name=form.username.data, isop=False, pin=calc_hash(form.pin.data))
                db.session.add(user)
                db.session.commit()

                flash('User successfully registered. Go to the login form to log in.', category='success')
                return redirect(url_for('auth.login'))

    return render_template('signup.html', form=form)
