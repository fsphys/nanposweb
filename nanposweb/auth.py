from flask import Blueprint, render_template, redirect, url_for, request, flash
from .models import User
from hashlib import sha256
from flask_login import login_required, logout_user, login_user

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('pin')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(name=username).first()

    if not user or sha256(password.encode('utf-8')).hexdigest() != user.pin:
        flash('Please check your login details and try again.', 'danger')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    flash('Logged in', 'success')
    return redirect(url_for('main.index'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out', 'success')
    return redirect(url_for('auth.login'))
