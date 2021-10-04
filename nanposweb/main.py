from flask import Blueprint, render_template
from .models import Product, Revenue
from .db import db
from flask_login import current_user, login_required

main = Blueprint('main', __name__)


@main.route('/')
@login_required
def index():
    products = Product.query.filter_by(visible=True).order_by(Product.name).all()
    stmt = db.select(db.func.sum(Revenue.amount)).where(Revenue.user == current_user.id)
    balance = db.session.execute(stmt).scalars().first()
    return render_template('index.html', products=products, user=current_user, balance=balance)


@main.route('/account')
@login_required
def account():
    return 'Account'
