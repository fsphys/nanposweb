from flask import Blueprint, render_template, flash, redirect, url_for, session
from flask_login import login_required
from flask_principal import Permission, RoleNeed

from ..db import db
from ..forms import ProductForm
from ..models import User, Product, Revenue

admin_bp = Blueprint('admin', __name__, url_prefix='/admin', template_folder='templates')

admin_permission = Permission(RoleNeed('admin'))


@admin_bp.route('/user')
@login_required
@admin_permission.require(http_exception=401)
def user():
    aggregation = db.select(db.func.sum(Revenue.amount).label('balance'), Revenue.user.label('user_id')).group_by(
        Revenue.user).subquery()
    user_query = db.select(User, db.func.coalesce(aggregation.c.balance, 0)).outerjoin(
        aggregation,
        User.id == aggregation.c.user_id
    ).order_by(User.name)
    users = db.session.execute(user_query).all()
    return render_template('user/view.html', users=users)


@admin_bp.route('/user/impersonate/<user_id>')
@login_required
@admin_permission.require(http_exception=401)
def impersonate(user_id):
    session['impersonate'] = user_id
    return redirect(url_for('main.index'))


@admin_bp.route('/user/impersonate/pop')
@login_required
@admin_permission.require(http_exception=401)
def pop_impersonate():
    session.pop('impersonate', None)
    return redirect(url_for('admin.user'))


@admin_bp.route('/product')
@login_required
@admin_permission.require(http_exception=401)
def product():
    products = Product.query.order_by(Product.name).all()
    return render_template('product/view.html', products=products)


@admin_bp.route('/product', methods=['POST'])
@login_required
@admin_permission.require(http_exception=401)
def product_post():
    form = ProductForm()
    if not form.validate_on_submit():
        flash('PANIC', 'danger')
        return render_template('product/form.html', form=form, edit=True)

    item = Product.query.filter_by(id=form.id.data).one_or_none()
    if item is None:
        new = Product(
            name=form.name.data,
            ean=form.ean.data,
            price=form.price.data,
            visible=form.visible.data,
            has_alc=form.has_alc.data,
            is_food=form.is_food.data
        )
        db.session.add(new)
        db.session.commit()
        flash(f'Created product "{form.name.data}"', 'success')
    else:
        item.name = form.name.data
        item.ean = form.ean.data
        item.price = form.price.data
        item.visible = form.visible.data
        item.has_alc = form.has_alc.data
        item.is_food = form.is_food.data
        db.session.commit()
        flash(f'Updated product "{form.name.data}"', 'success')

    return redirect(url_for('admin.product'))


@admin_bp.route('/product/add')
@login_required
@admin_permission.require(http_exception=401)
def product_add():
    form = ProductForm()
    return render_template('product/form.html', form=form, edit=False)


@admin_bp.route('/product/edit/<product_id>')
@login_required
@admin_permission.require(http_exception=401)
def product_edit(product_id):
    item = Product.query.filter_by(id=product_id).one()
    form = ProductForm(
        id=item.id,
        name=item.name,
        ean=item.ean,
        price=item.price,
        visible=item.visible,
        has_alc=item.has_alc,
        is_food=item.is_food,
    )
    return render_template('product/form.html', form=form, edit=True)


@admin_bp.route('/product/delete/<product_id>')
@login_required
@admin_permission.require(http_exception=401)
def product_delete(product_id):
    item = Product.query.filter_by(id=product_id).one()
    db.session.delete(item)
    db.session.commit()
    flash(f'Deleted product "{item.name}"', 'success')
    return redirect(url_for('admin.product'))
