from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.fields.html5 import IntegerField
from wtforms.validators import InputRequired, Optional
from wtforms_html5 import AutoAttrMeta


class MainForm(FlaskForm):
    class Meta(AutoAttrMeta):
        pass

    pass


class ProductForm(FlaskForm):
    class Meta(AutoAttrMeta):
        pass

    id = IntegerField(label='ID', render_kw={'placeholder': 'id', 'readonly': ''}, )
    name = StringField(label='Name', validators=[InputRequired()], render_kw={'placeholder': 'name'}, )
    ean = IntegerField(label='EAN', validators=[Optional(strip_whitespace=True)], render_kw={'placeholder': 'ean'})
    price = IntegerField(label='Price', validators=[InputRequired()], render_kw={'placeholder': 'price'}, )
    visible = BooleanField(label='Visible', )
    has_alc = BooleanField(label='Has Alcohol', )
    is_food = BooleanField(label='Is Food', )
