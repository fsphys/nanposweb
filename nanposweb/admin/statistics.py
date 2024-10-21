from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required
from sqlalchemy import func

from ..db import db
from ..db.models import Product, Revenue, User
from .helpers import admin_permission

statistics_bp = Blueprint('statistics', __name__, url_prefix='/statistics')


@statistics_bp.route('/')
@login_required
@admin_permission.require(http_exception=401)
def index():
    # Get a list of all paid
    products = Product.query.order_by(Product.name).filter(Product.price > 0).all()

    results = []

    for product in products:
        max_revenue = Revenue.query.with_entities(Revenue.user, func.count(Revenue.user)).where(
            Revenue.product == product.id).group_by(Revenue.user).all()

        maximum = 0
        users = []

        for revenue in max_revenue:
            if revenue[1] > maximum:
                maximum = revenue[1]
                user_query = User.query.filter(User.id == revenue[0]).all()
                users = [u for u in user_query]
            elif revenue[1] == maximum:
                # Append the current user
                user_query = User.query.filter(User.id == revenue[0]).all()
                for u in user_query:
                    users.append(u)

        results.append({"product": product, "count": maximum, "users": users})

    total_balance = Revenue.query.with_entities(func.sum(Revenue.amount).label('total')).first().total
    total_user_count = User.query.with_entities(func.count(User.id)).scalar()
    total_product_count = Product.query.with_entities(func.count(Product.id)).scalar()

    return render_template('statistics/index.html', results=results, total_balance=total_balance,
                           total_user_count=total_user_count, total_product_count=total_product_count)
