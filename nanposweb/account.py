from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from wtforms.validators import InputRequired

from .db import db
from .forms import PinForm, CardForm
from .db.models import Revenue, Product
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

    no_pin_attrs = ['readonly', 'disabled']
    if current_user.pin is None:
        for item in no_pin_attrs:
            form.old_pin.render_kw[item] = ''
        form.old_pin.validators = []
    else:
        for item in no_pin_attrs:
            form.old_pin.render_kw.pop(item, None)
        form.old_pin.validators = [InputRequired()]

    if form.validate_on_submit():
        if current_user.pin is not None:
            if not check_hash(current_user.pin, form.old_pin.data):
                flash('Old PIN is not correct', 'danger')
                return render_template('account/change_pin.html', form=form)

        if form.new_pin.data != form.confirm_pin.data:
            flash('New PIN and Confirmation do not match', 'danger')
            return render_template('account/change_pin.html', form=form)

        if form.unset_pin.data:
            current_user.pin = None
            flash('Unset PIN', 'success')
        else:
            current_user.pin = calc_hash(form.new_pin.data)
            flash('Changed PIN', 'success')

        db.session.commit()
        return redirect(url_for('account.index'))

    return render_template('account/change_pin.html', form=form)


@account_bp.route('/card', methods=['GET', 'POST'])
@login_required
def card():
    form = CardForm()

    if form.validate_on_submit():
        if form.unset_card.data:
            current_user.card = None
            flash('Unset Card', 'success')
        else:
            current_user.card = calc_hash(form.card_number.data)
            flash('Changed Card', 'success')

        db.session.commit()
        return redirect(url_for('account.index'))

    return render_template('account/change_card.html', form=form)
