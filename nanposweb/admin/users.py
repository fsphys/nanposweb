from flask import Blueprint, render_template, redirect, url_for, session
from flask_login import login_required

from .util import admin_permission
from ..db import db
from ..models import User, Revenue

users_bp = Blueprint('users', __name__, url_prefix='/users')


@users_bp.route('/')
@login_required
@admin_permission.require(http_exception=401)
def index():
    aggregation = db.select(db.func.sum(Revenue.amount).label('balance'), Revenue.user.label('user_id')).group_by(
        Revenue.user).subquery()
    user_query = db.select(User, db.func.coalesce(aggregation.c.balance, 0)).outerjoin(
        aggregation,
        User.id == aggregation.c.user_id
    ).order_by(User.name)
    users_list = db.session.execute(user_query).all()
    return render_template('users/index.html', users=users_list)


@users_bp.route('/impersonate/<user_id>')
@login_required
@admin_permission.require(http_exception=401)
def impersonate(user_id):
    session['impersonate'] = user_id
    return redirect(url_for('main.index'))


@users_bp.route('/impersonate/pop')
@login_required
@admin_permission.require(http_exception=401)
def pop_impersonate():
    session.pop('impersonate', None)
    return redirect(url_for('admin.users.index'))
