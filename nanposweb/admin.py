from flask import Blueprint, render_template
from flask_login import login_required

from .db import db
from .models import User, Product, Revenue
from .util import admin_required

admin = Blueprint('admin', __name__)


@admin.route('/admin')
@login_required
@admin_required
def index():
    aggregation = db.select(db.func.sum(Revenue.amount).label('balance'), Revenue.user.label('user_id')).group_by(
        Revenue.user).subquery()
    user_query = db.select(User, db.func.coalesce(aggregation.c.user_id, 0)).outerjoin(
        aggregation,
        User.id == aggregation.c.user_id
    ).order_by(User.name)
    users = db.session.execute(user_query).all()
    products = Product.query.order_by(Product.name).all()
    return render_template('admin.html', users=users, products=products)
