from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import current_user, login_required

from .db import db
from .forms import MainForm
from .models import Product, Revenue, User
from .util import format_currency
from .admin import admin_permission

main = Blueprint('main', __name__)


@main.context_processor
def impersonate():
    impersonate_user_id = session.get('impersonate', None)
    impersonate_user = User.query.get(impersonate_user_id)
    user_name = impersonate_user.name if impersonate_user_id else current_user.name
    return dict(impersonate_user=impersonate_user, user_name=user_name)


@main.route('/')
@login_required
def index():
    impersonate_user_id = session.get('impersonate', None)
    if impersonate_user_id is not None:
        user_id = impersonate_user_id
    else:
        user_id = current_user.id
    stmt = db.select(db.func.coalesce(db.func.sum(Revenue.amount), 0)).where(Revenue.user == user_id)
    balance = db.session.execute(stmt).scalars().first()

    view_all = request.args.get('view_all', False)
    form = MainForm()
    products = Product.query.order_by(Product.name).all()
    return render_template('index.html', products=products, balance=balance, form=form, view_all=view_all)


@main.route('/', methods=['POST'])
@login_required
def index_post():
    impersonate_user_id = session.get('impersonate', None)
    if admin_permission.can() and impersonate_user_id:
        user = User.query.get(impersonate_user_id)
        user_id = user.id
        user_message = f' as {user.name}'
    else:
        user_id = current_user.id
        user_message = ''

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

    rev = Revenue(user=user_id, product=product.id, amount=-product.price)
    db.session.add(rev)
    db.session.commit()

    # remove impersonate session state
    session.pop('impersonate', None)

    flash(f'Bought {product.name} for {format_currency(product.price)}{user_message}', 'success')
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
