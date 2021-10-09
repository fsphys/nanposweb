from hashlib import sha256

from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, session
from flask_login import login_required, logout_user, login_user
from flask_principal import identity_changed, Identity, AnonymousIdentity

from .forms import LoginForm
from .models import User

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(name=form.username.data).one_or_none()

        if user and sha256(form.pin.data.encode('utf-8')).hexdigest() == user.pin:
            login_user(user, remember=form.remember.data)
            flash('Logged in', 'success')

            identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))

            return redirect(request.args.get('next') or url_for('main.index'))
        else:
            flash('Please check your login details and try again.', 'danger')

    return render_template('login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()

    # Remove session keys set by Flask-Principal
    for key in ('identity.id', 'identity.auth_type'):
        session.pop(key, None)

    session.pop('impersonate', None)

    # Tell Flask-Principal the user is anonymous
    identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())
    flash('Logged out', 'success')
    return redirect(url_for('auth.login'))
