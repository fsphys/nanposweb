from . import db
from .models import Revenue


def get_balance(user_id):
    stmt = db.select(db.func.coalesce(db.func.sum(Revenue.amount), 0)).where(Revenue.user == user_id)
    balance = db.session.execute(stmt).scalars().first()
    return balance
