from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import InputRequired
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


class PinForm(FlaskForm):
    class Meta(AutoAttrMeta):
        pass

    old_pin = PasswordField(label='Old PIN', validators=[InputRequired()], render_kw={'placeholder': 'pin'}, )
    unset_pin = BooleanField(label='Unset PIN', )
    new_pin = PasswordField(label='New PIN', render_kw={'placeholder': 'pin'}, )
    confirm_pin = PasswordField(label='Confirm new PIN', render_kw={'placeholder': 'pin'}, )


class CardForm(FlaskForm):
    class Meta(AutoAttrMeta):
        pass

    card_number = StringField(label='Card ID', render_kw={'placeholder': 'Card ID'}, )
    unset_card = BooleanField(label='Unset Card', )
