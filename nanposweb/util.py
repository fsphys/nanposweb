from functools import wraps

from flask import current_app, redirect, url_for, flash
from flask_login import current_user


def format_currency(value, factor=100):
    return '{:.2f} €'.format(value / factor).replace('.', ',')


def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_app.config.get('LOGIN_DISABLED'):
            return func(*args, **kwargs)
        elif not current_user.isop:
            flash(f'You are not allowed to access this page.', 'danger')
            return redirect(url_for('main.index'))
        return func(*args, **kwargs)

    return decorated_view
