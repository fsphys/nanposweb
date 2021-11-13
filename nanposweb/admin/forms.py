from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, PasswordField, IntegerField, DecimalField
from wtforms.validators import InputRequired, Optional


class ProductForm(FlaskForm):
    id = IntegerField(label='ID', render_kw={'placeholder': 'id', 'readonly': ''}, )
    name = StringField(label='Name', validators=[InputRequired()], render_kw={'placeholder': 'name'}, )
    ean = IntegerField(label='EAN', validators=[Optional(strip_whitespace=True)], render_kw={'placeholder': 'ean'}, )
    price = IntegerField(label='Price', validators=[InputRequired()], render_kw={'placeholder': 'price'}, )
    visible = BooleanField(label='Visible', )
    has_alc = BooleanField(label='Has Alcohol', )
    is_food = BooleanField(label='Is Food', )


class UserForm(FlaskForm):
    id = IntegerField(label='ID', render_kw={'placeholder': 'id', 'readonly': ''}, )
    name = StringField(label='Name', validators=[InputRequired()], render_kw={'placeholder': 'name'}, )
    card = StringField(label='Card ID', render_kw={'placeholder': 'Card ID'}, )
    unset_card = BooleanField(label='Unset Card', )
    pin = PasswordField(label='PIN', render_kw={'placeholder': 'pin'}, )
    unset_pin = BooleanField(label='Unset PIN', )
    isop = BooleanField(label='Admin', )


class BalanceForm(FlaskForm):
    amount = DecimalField(label='Amount', validators=[InputRequired()], render_kw={'placeholder': '0.00'}, )
    recharge = SubmitField(label='Recharge')
    charge = SubmitField(label='Charge')
