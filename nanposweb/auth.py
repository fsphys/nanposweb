from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, session
from flask_login import login_required, logout_user, login_user, current_user
from flask_principal import identity_changed, Identity, AnonymousIdentity

from .db.models import User
from .forms import LoginForm
from .helpers import check_hash

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('Already logged in.')
        return redirect(request.args.get('next') or url_for('main.index'))

    session['terminal'] = request.args.get('terminal', False, type=bool)
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(name=form.username.data).one_or_none()

        if user and check_hash(user.pin, form.pin.data):
            login_user(user, remember=form.remember.data)
            flash('Logged in', 'success')

            identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))

            return redirect(request.args.get('next') or url_for('main.index'))
        else:
            flash('Please check your login details and try again.', 'danger')

    return render_template('login.html', form=form)


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
