from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField, IntegerField, HiddenField
from wtforms.validators import InputRequired, Optional


class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[InputRequired()],
                           render_kw={'placeholder': 'Username', 'autofocus': True}, )
    pin = PasswordField(label='PIN', validators=[InputRequired()], render_kw={'placeholder': 'PIN'}, )
    remember = BooleanField(label='Remember me', )
    submit = SubmitField(label='Sign in', )


class CardLoginForm(FlaskForm):
    card = HiddenField(label="Card", validators=[InputRequired()])
    reader = HiddenField(label="Reader", validators=[InputRequired()])


class SignUpForm(FlaskForm):
    username = StringField(label='Username', validators=[InputRequired()],
                           render_kw={'placeholder': 'Username', 'autofocus': True}, )
    pin = PasswordField(label='PIN', validators=[InputRequired()], render_kw={'placeholder': 'PIN'}, )
    repeat_pin = PasswordField(label='Repeat PIN', validators=[InputRequired()], render_kw={'placeholder': 'PIN'}, )
    submit = SubmitField(label='Sign up', )


class MainForm(FlaskForm):
    ean = IntegerField(label='EAN', validators=[Optional()], render_kw={'placeholder': 'EAN', 'autofocus': True}, )


class PinForm(FlaskForm):
    old_pin = PasswordField(label='Old PIN', validators=[InputRequired()], render_kw={'placeholder': 'pin'}, )
    unset_pin = BooleanField(label='Unset PIN', )
    new_pin = PasswordField(label='New PIN', render_kw={'placeholder': 'pin'}, )
    confirm_pin = PasswordField(label='Confirm new PIN', render_kw={'placeholder': 'pin'}, )
    change_pin = SubmitField(label='Change PIN', )


class CardForm(FlaskForm):
    card_number = StringField(label='Card ID', render_kw={'placeholder': 'Card ID'}, )
    unset_card = BooleanField(label='Unset Card', )
    change_card = SubmitField(label='Change Card', )
