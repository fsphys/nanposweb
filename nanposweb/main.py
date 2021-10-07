from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required

from .db import db
from .forms import MainForm
from .models import Product, Revenue
from .util import format_currency

main = Blueprint('main', __name__)


@main.route('/')
@login_required
def index():
    view_all = request.args.get('view_all', False)
    form = MainForm()
    products = Product.query.order_by(Product.name).all()
    stmt = db.select(db.func.sum(Revenue.amount)).where(Revenue.user == current_user.id)
    balance = db.session.execute(stmt).scalars().first()
    return render_template('index.html', products=products, balance=balance, form=form, view_all=view_all)


@main.route('/', methods=['POST'])
@login_required
def index_post():
    form = MainForm()
    if not form.validate_on_submit():
        flash('PANIC', 'danger')
        return redirect(url_for('main.index'))

    product_id = request.form.get('product_id')
    if product_id is None:
        flash('No product id given', 'danger')

    product = Product.query.filter_by(id=product_id).first()
    if product is None:
        flash(f'No product with id {product_id} known.', 'danger')

    rev = Revenue(user=current_user.id, product=product.id, amount=-product.price)
    db.session.add(rev)
    db.session.commit()

    flash(f'Buyed {product.name} for {format_currency(product.price)}', 'success')
    return redirect(url_for('main.index'))


@main.route('/account')
@login_required
def account():
    stmt = db.select(db.func.sum(Revenue.amount)).where(Revenue.user == current_user.id)
    balance = db.session.execute(stmt).scalars().first()
    revenues_query = db.select(Revenue, db.func.coalesce(Product.name, '')).outerjoin(
        Product, Revenue.product == Product.id).where(Revenue.user == current_user.id).order_by(db.desc(Revenue.id))
    revenues = db.session.execute(revenues_query).all()
    return render_template('account.html', balance=balance, revenues=revenues)
