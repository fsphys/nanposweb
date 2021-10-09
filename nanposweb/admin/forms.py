from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, PasswordField
from wtforms.fields.html5 import IntegerField, DecimalField
from wtforms.validators import InputRequired, Optional
from wtforms_html5 import AutoAttrMeta


class ProductForm(FlaskForm):
    class Meta(AutoAttrMeta):
        pass

    id = IntegerField(label='ID', render_kw={'placeholder': 'id', 'readonly': ''}, )
    name = StringField(label='Name', validators=[InputRequired()], render_kw={'placeholder': 'name'}, )
    ean = IntegerField(label='EAN', validators=[Optional(strip_whitespace=True)], render_kw={'placeholder': 'ean'}, )
    price = IntegerField(label='Price', validators=[InputRequired()], render_kw={'placeholder': 'price'}, )
    visible = BooleanField(label='Visible', )
    has_alc = BooleanField(label='Has Alcohol', )
    is_food = BooleanField(label='Is Food', )


class UserForm(FlaskForm):
    class Meta(AutoAttrMeta):
        pass

    name = StringField(label='Name', validators=[InputRequired()], render_kw={'placeholder': 'name'}, )
    card = StringField(label='Card ID', render_kw={'placeholder': 'Card ID'}, )
    pin = PasswordField(label='New PIN', render_kw={'placeholder': 'pin'}, )


class BalanceForm(FlaskForm):
    class Meta(AutoAttrMeta):
        pass

    amount = DecimalField(label='Amount', validators=[InputRequired()], render_kw={'placeholder': '0.00'}, )
    recharge = SubmitField(label='Recharge')
    charge = SubmitField(label='Charge')
