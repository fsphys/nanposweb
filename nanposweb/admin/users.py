from flask import Blueprint, render_template, redirect, url_for, session, flash
from flask_login import login_required

from .forms import BalanceForm, UserForm
from .util import admin_permission
from ..db import db
from ..db.models import User, Revenue
from ..util import calc_hash

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


@users_bp.route('/', methods=['POST'])
@login_required
@admin_permission.require(http_exception=401)
def post():
    form = UserForm()
    if not form.validate_on_submit():
        flash('PANIC', 'danger')
        return render_template('products/form.html', form=form, edit=True)

    create = False
    user = User.query.filter_by(id=form.id.data).one_or_none()
    if user is None:
        create = True
        user = User()

    user.name = form.name.data
    user.isop = form.isop.data

    if form.unset_pin.data:
        user.pin = None
    elif form.pin.data != '':
        user.pin = calc_hash(form.pin.data)

    if form.unset_card.data:
        user.card = None
    elif form.card.data != '':
        user.card = calc_hash(form.card.data)

    if create:
        db.session.add(user)
        db.session.commit()
        flash(f'Created user {form.name.data}', 'success')
    else:
        db.session.commit()
        flash(f'Updated user "{form.name.data}"', 'success')

    return redirect(url_for('admin.users.index'))


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


@users_bp.route('/balance/<user_id>', methods=['GET', 'POST'])
@login_required
@admin_permission.require(http_exception=401)
def balance(user_id):
    user = User.query.get(int(user_id))
    form = BalanceForm()

    if form.validate_on_submit():
        euros = form.amount.data
        cents = int(euros * 100)

        if form.recharge.data:
            factor = 1
            flash(f'Added {euros:.2f} € for {user.name}', 'success')
        elif form.charge.data:
            factor = -1
            flash(f'Charged {euros:.2f} € from {user.name}', 'success')
        else:
            flash('PANIC', 'danger')
            return render_template('users/balance.html', form=form, user=user)

        rev = Revenue(user=user.id, product=None, amount=cents * factor)
        db.session.add(rev)
        db.session.commit()
        return redirect(url_for('admin.users.index'))

    return render_template('users/balance.html', form=form, user=user)


@users_bp.route('/add')
@login_required
@admin_permission.require(http_exception=401)
def add():
    form = UserForm()
    return render_template('users/form.html', form=form, edit=False)


@users_bp.route('/edit/<user_id>')
@login_required
@admin_permission.require(http_exception=401)
def edit(user_id):
    user = User.query.get(int(user_id))
    form = UserForm(
        id=user.id,
        name=user.name,
        isop=user.isop
    )

    return render_template('users/form.html', form=form, edit=True)


@users_bp.route('/delete/<user_id>')
@login_required
@admin_permission.require(http_exception=401)
def delete(user_id):
    user = User.query.get(int(user_id))
    db.session.delete(user)
    db.session.commit()
    flash(f'Deleted user "{user.name}"', 'success')
    return redirect(url_for('admin.users.index'))
