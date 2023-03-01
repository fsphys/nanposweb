from . import db
from .models import Revenue, Product


def get_balance(user_id):
    """
    Query the revenues to determine the current balance of the specified user
    :param user_id: Valid user id
    :return: Balance of the specified user in cents as an integer
    """
    stmt = db.select(db.func.coalesce(db.func.sum(Revenue.amount), 0)).where(Revenue.user == user_id)
    balance = db.session.execute(stmt).scalars().first()
    return balance


def revenue_query(user_id):
    revenues_query = db.select(Revenue, db.func.coalesce(Product.name, '')).outerjoin(
        Product, Revenue.product == Product.id).where(Revenue.user == user_id).order_by(db.desc(Revenue.date))
    return revenues_query
