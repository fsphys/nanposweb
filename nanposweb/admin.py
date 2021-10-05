from flask import Blueprint, render_template
from flask_login import login_required

from .models import User, Product
from .util import admin_required

admin = Blueprint('admin', __name__)


@admin.route('/admin')
@login_required
@admin_required
def index():
    users = User.query.order_by(User.name).all()
    products = Product.query.order_by(Product.name).all()
    return render_template('admin.html', users=users, products=products)
