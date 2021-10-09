from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_required

from .db import db
from .forms import PinForm, CardForm
from .models import Revenue, Product
from .util import check_hash, calc_hash

account_bp = Blueprint('account', __name__, url_prefix='/account')


@account_bp.route('/')
@login_required
def index():
    stmt = db.select(db.func.sum(Revenue.amount)).where(Revenue.user == current_user.id)
    balance = db.session.execute(stmt).scalars().first()
    revenues_query = db.select(Revenue, db.func.coalesce(Product.name, '')).outerjoin(
        Product, Revenue.product == Product.id).where(Revenue.user == current_user.id).order_by(db.desc(Revenue.id))
    revenues = db.session.execute(revenues_query).all()
    return render_template('account/index.html', balance=balance, revenues=revenues)


@account_bp.route('/pin', methods=['GET', 'POST'])
@login_required
def pin():
    form = PinForm()

    if form.validate_on_submit():
        if not check_hash(current_user.pin, form.old_pin.data):
            flash('Old PIN is not correct', 'danger')
            return render_template('account/change_pin.html', form=form)

        if form.new_pin.data != form.confirm_pin.data:
            flash('New PIN and Confirmation do not match', 'danger')
            return render_template('account/change_pin.html', form=form)

        if form.new_pin.data != '':
            current_user.pin = calc_hash(form.new_pin.data)
        else:
            current_user.pin = None

        db.session.commit()

        flash('Changed PIN', 'success')
        return redirect(url_for('account.index'))

    return render_template('account/change_pin.html', form=form)


@account_bp.route('/card', methods=['GET', 'POST'])
@login_required
def card():
    user_card = 'set' if current_user.card else ''
    form = CardForm(card_number=user_card)

    if form.validate_on_submit() and form.card_number.data != 'set':
        if form.card_number.data != '':
            current_user.card = calc_hash(form.card_number.data)
        else:
            current_user.card = None

        db.session.commit()

        flash('Changed Card', 'success')
        return redirect(url_for('account.index'))

    return render_template('account/change_card.html', form=form)
