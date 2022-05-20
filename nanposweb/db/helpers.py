from . import db
from .models import Revenue, Product


def get_balance(user_id):
    stmt = db.select(db.func.coalesce(db.func.sum(Revenue.amount), 0)).where(Revenue.user == user_id)
    balance = db.session.execute(stmt).scalars().first()
    return balance


def revenue_query(user_id):
    revenues_query = db.select(Revenue, db.func.coalesce(Product.name, '')).outerjoin(
        Product, Revenue.product == Product.id).where(Revenue.user == user_id).order_by(db.desc(Revenue.date))
    return revenues_query
