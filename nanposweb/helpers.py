from hashlib import sha256
from flask import session, current_app
from flask_login import current_user
from .db.models import Revenue


def format_currency(value, factor=100):
    return '{:.2f} €'.format(value / factor).replace('.', ',')


def check_hash(_hash, value):
    hashed_value = sha256(value.encode('utf-8')).hexdigest()

    if _hash == hashed_value:
        return True
    else:
        return False


def calc_hash(value):
    return sha256(value.encode('utf-8')).hexdigest()


def get_user_id():
    impersonate_user_id = session.get('impersonate', None)
    if impersonate_user_id is not None:
        user_id = impersonate_user_id
    else:
        user_id = current_user.id
    return user_id


def revenue_is_cancelable(revenue: Revenue) -> bool:
    return revenue.age.total_seconds() < current_app.config.get('QUICK_CANCEL_SEC')


def revenue_in_cooldown(revenue: Revenue) -> bool:
    return revenue.age.total_seconds() < current_app.config.get("PURCHASE_COOLDOWN")
