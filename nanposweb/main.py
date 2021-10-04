from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required

from .db import db
from .models import Product, Revenue
from .util import format_currency

main = Blueprint('main', __name__)


@main.route('/')
@login_required
def index():
    products = Product.query.filter_by(visible=True).order_by(Product.name).all()
    stmt = db.select(db.func.sum(Revenue.amount)).where(Revenue.user == current_user.id)
    balance = db.session.execute(stmt).scalars().first()
    return render_template('index.html', products=products, user=current_user, balance=balance)


@main.route('/', methods=['POST'])
@login_required
def index_post():
    product_id = request.form.get('product_id')
    if product_id is None:
        flash(f'No product id given', 'danger')

    product = Product.query.filter_by(id=product_id).first()
    if product is None:
        flash(f'No product with id {product_id} known.', 'danger')

    rev = Revenue(user=current_user.id, product=product.id, amount=product.price)
    db.session.add(rev)
    db.session.commit()

    flash(f'Buyed {product.name} for {format_currency(product.price)}', 'success')
    return redirect(url_for('main.index'))


@main.route('/account')
@login_required
def account():
    return 'Account'
