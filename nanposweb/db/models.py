from datetime import datetime
from flask_login import UserMixin

from . import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.VARCHAR(200), nullable=False, unique=True)
    card = db.Column('card', db.VARCHAR(500))
    isop = db.Column('isop', db.Boolean, server_default=db.false(), nullable=False)
    pin = db.Column('pin', db.VARCHAR(500))


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.VARCHAR(50), nullable=False, unique=True)
    ean = db.Column('ean', db.BigInteger, unique=True)
    price = db.Column('price', db.Integer, nullable=False)
    visible = db.Column('visible', db.Boolean, nullable=False, server_default=db.true())
    has_alc = db.Column('has_alc', db.Boolean, nullable=False, server_default=db.false())
    is_food = db.Column('is_food', db.Boolean, nullable=False, server_default=db.false())


class Revenue(db.Model):
    __tablename__ = 'revenues'
    id = db.Column('id', db.Integer, primary_key=True)
    user = db.Column('user', db.Integer, db.ForeignKey('users.id'), nullable=False)
    product = db.Column('product', db.Integer, db.ForeignKey('products.id'))
    amount = db.Column('amount', db.Integer, nullable=False)
    date = db.Column('date', db.TIMESTAMP(timezone=True), server_default=db.func.now())

    @property
    def age(self):
        """
        Method to calculate the age of the purchase.

        :return: naive datetime offset representing the age of the revenue
        """

        # As most databases (Postgres, SQLite) store time zone aware internal as UTC with the matching offset, the
        # returned datetime object from the sqlalchemy will be an utc date with the additional timezone information. If
        # we strip that information to get a naive date, we need to consider, that is a UTC date.
        date_naive = self.date.replace(tzinfo=None)
        # We can't ensure, that our system is running in the UTC timezone. To get the correct current time now() can't
        # be used, as it returns the naive, local datetime. Therefore, utcnow() is used to get a naive UTC datetime.
        age = datetime.utcnow() - date_naive
        return age
