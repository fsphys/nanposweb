from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required

from .forms import ProductForm
from .util import admin_permission
from ..db import db
from ..models import Product

products_bp = Blueprint('products', __name__, url_prefix='/products')


@products_bp.route('/')
@login_required
@admin_permission.require(http_exception=401)
def index():
    products = Product.query.order_by(Product.name).all()
    return render_template('products/index.html', products=products)


@products_bp.route('/', methods=['POST'])
@login_required
@admin_permission.require(http_exception=401)
def post():
    form = ProductForm()
    if not form.validate_on_submit():
        flash('PANIC', 'danger')
        return render_template('products/form.html', form=form, edit=True)

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
        flash(f'Created products "{form.name.data}"', 'success')
    else:
        item.name = form.name.data
        item.ean = form.ean.data
        item.price = form.price.data
        item.visible = form.visible.data
        item.has_alc = form.has_alc.data
        item.is_food = form.is_food.data
        db.session.commit()
        flash(f'Updated products "{form.name.data}"', 'success')

    return redirect(url_for('admin.products.index'))


@products_bp.route('/add')
@login_required
@admin_permission.require(http_exception=401)
def add():
    form = ProductForm()
    return render_template('products/form.html', form=form, edit=False)


@products_bp.route('/edit/<product_id>')
@login_required
@admin_permission.require(http_exception=401)
def edit(product_id):
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
    return render_template('products/form.html', form=form, edit=True)


@products_bp.route('/delete/<product_id>')
@login_required
@admin_permission.require(http_exception=401)
def delete(product_id):
    product = Product.query.get(int(product_id))
    db.session.delete(product)
    db.session.commit()
    flash(f'Deleted product "{product.name}"', 'success')
    return redirect(url_for('admin.products.index'))
