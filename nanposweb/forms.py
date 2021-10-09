from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.fields.html5 import IntegerField
from wtforms.validators import InputRequired, Optional
from wtforms_html5 import AutoAttrMeta


class LoginForm(FlaskForm):
    class Meta(AutoAttrMeta):
        pass

    username = StringField(label='Username', validators=[InputRequired()], render_kw={'placeholder': 'Username'}, )
    pin = PasswordField(label='PIN', validators=[InputRequired()], render_kw={'placeholder': 'PIN'}, )
    remember = BooleanField(label='Remember me', )
    submit = SubmitField(label='Sign in', )


class MainForm(FlaskForm):
    class Meta(AutoAttrMeta):
        pass

    pass


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


class PinForm(FlaskForm):
    class Meta(AutoAttrMeta):
        pass

    old_pin = PasswordField(label='Old PIN', validators=[InputRequired()], render_kw={'placeholder': 'pin'}, )
    new_pin = PasswordField(label='New PIN', validators=[InputRequired()], render_kw={'placeholder': 'pin'}, )
    confirm_pin = PasswordField(label='Confirm new PIN', validators=[InputRequired()],
                                render_kw={'placeholder': 'pin'}, )
