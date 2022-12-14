from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from wtforms.validators import InputRequired

from .db import db
from .db.helpers import get_balance, revenue_query
from .forms import PinForm, CardForm
from .helpers import check_hash, calc_hash

account_bp = Blueprint('account', __name__, url_prefix='/account')


@account_bp.route('/')
@login_required
def index():
    balance = get_balance(current_user.id)
    revenues_query = revenue_query(current_user.id)
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

    if request.method == 'POST':
        if form.validate_on_submit():
            if current_user.pin is not None:
                if not check_hash(current_user.pin, form.old_pin.data):
                    flash('Old PIN is not correct', category='danger')
                    return render_template('account/change_pin.html', form=form)

            if form.new_pin.data != form.confirm_pin.data:
                flash('New PIN and Confirmation do not match', category='danger')
                return render_template('account/change_pin.html', form=form)

            if form.unset_pin.data:
                current_user.pin = None
                flash('Unset PIN', category='success')
            else:
                current_user.pin = calc_hash(form.new_pin.data)
                flash('Changed PIN', category='success')

            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            flash('Submitted form was not valid!', category='danger')

    return render_template('account/change_pin.html', form=form)


@account_bp.route('/card', methods=['GET', 'POST'])
@login_required
def card():
    form = CardForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            if form.unset_card.data:
                current_user.card = None
                flash('Unset Card', category='success')
            else:
                current_user.card = calc_hash(form.card_number.data)
                flash('Changed Card', category='success')

            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            flash('Submitted form was not valid!', category='danger')

    return render_template('account/change_card.html', form=form)
