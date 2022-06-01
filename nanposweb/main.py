import datetime

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from flask_login import current_user, login_required

from .admin.helpers import admin_permission
from .db import db
from .db.helpers import get_balance, revenue_query
from .db.models import Product, Revenue, User
from .forms import MainForm
from .helpers import format_currency, get_user_id, revenue_is_canceable

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
    user_id = get_user_id()
    balance = get_balance(user_id)

    last_buy_query = revenue_query(user_id)
    last_revenue, last_revenue_product_name = db.session.execute(last_buy_query).first() or (None, None)

    if last_revenue is not None and not revenue_is_canceable(last_revenue):
        last_revenue = False

    most_buyed_timestamp = datetime.datetime.now() - datetime.timedelta(days=current_app.config['FAVORITES_DAYS'])
    most_buyed_query = db.select(Product, db.func.count(Revenue.product).label('CTR')).join(Product).where(
        Revenue.product is not None).where(Revenue.user == user_id).where(Revenue.date >= most_buyed_timestamp).group_by(Product.id).order_by(db.desc('CTR'))
    most_buyed = db.session.execute(most_buyed_query).all()
    favorites = [f[0] for f in most_buyed[:current_app.config.get('FAVORITES_DISPLAY')]]

    view_all = request.args.get('view_all', False, type=bool)
    form = MainForm()
    products = Product.query.order_by(Product.name).all()
    return render_template('index.html', products=products, balance=balance, form=form, view_all=view_all,
                           favorites=favorites, last_revenue=last_revenue,
                           last_revenue_product_name=last_revenue_product_name)


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


@main_bp.route('/quick-cancel', methods=['GET'])
@login_required
def quick_cancel():
    user_id = get_user_id()
    last_buy_query = revenue_query(user_id)
    last_revenue, last_revenue_product_name = db.session.execute(last_buy_query).first()

    if revenue_is_canceable(last_revenue):
        db.session.delete(last_revenue)
        db.session.commit()
        flash(f'Canceled revenue: {last_revenue_product_name} for {format_currency(last_revenue.amount)}',
              category='success')
    else:
        flash(f'Could not cancel revenue: {last_revenue_product_name} for {format_currency(last_revenue.amount)}'
              f'</br> because its too old:'
              f' {round(last_revenue.age.total_seconds())}s > {current_app.config.get("QUICK_CANCEL_SEC")}s',
              category='danger')

    return redirect(url_for('main.index'))


@main_bp.route('/bank-account', methods=['GET'])
def bank_account():
    return render_template('bank_account.html', bank_data=current_app.config.get('BANK_DATA'))
