from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from flask_login import current_user, login_required

from .admin.helpers import admin_permission
from .db import db
from .db.models import Product, Revenue, User
from .db.helpers import get_balance
from .forms import MainForm
from .helpers import format_currency

main_bp = Blueprint('main', __name__)


@main_bp.context_processor
def impersonate():
    if current_user.is_authenticated:
        impersonate_user_id = session.get('impersonate', None)
        if impersonate_user_id is not None:
            impersonate_user = User.query.get(impersonate_user_id)
        else:
            impersonate_user = None
        user_name = impersonate_user.name if impersonate_user_id else current_user.name
        return dict(impersonate_user=impersonate_user, user_name=user_name)
    else:
        return dict()


@main_bp.route('/')
@login_required
def index():
    impersonate_user_id = session.get('impersonate', None)
    if impersonate_user_id is not None:
        user_id = impersonate_user_id
    else:
        user_id = current_user.id
    balance = get_balance(user_id)

    view_all = request.args.get('view_all', False, type=bool)
    form = MainForm()
    products = Product.query.order_by(Product.name).all()
    return render_template('index.html', products=products, balance=balance, form=form, view_all=view_all)


@main_bp.route('/', methods=['POST'])
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
        flash('Submitted form was not valid!', category='danger')
        return redirect(url_for('main.index'))

    if form.ean.data:
        ean = form.ean.data
        product = Product.query.filter_by(ean=ean).first()
        if product is None:
            flash(f'No product with ean {ean} known.', category='danger')
            return redirect(url_for('main.index'))
    else:
        product_id = request.form.get('product_id')
        if product_id is None:
            flash('No product id given', category='danger')
            return redirect(url_for('main.index'))

        product = Product.query.filter_by(id=product_id).first()
        if product is None:
            flash(f'No product with id {product_id} known.', category='danger')
            return redirect(url_for('main.index'))

    rev = Revenue(user=user_id, product=product.id, amount=-product.price)
    db.session.add(rev)
    db.session.commit()

    # remove impersonate session state
    session.pop('impersonate', None)

    flash(f'Bought {product.name} for {format_currency(product.price)}{user_message}', category='success')
    if session.get('terminal', False):
        return redirect(url_for('auth.logout'))
    else:
        if impersonate_user_id is not None:
            return redirect(url_for('admin.users.index'))
        else:
            return redirect(url_for('main.index'))


@main_bp.route('/bankaccount', methods=['GET'])
def bank_account():
    return render_template('bank_account.html', bank_data=current_app.config.get('BANK_DATA', None))
