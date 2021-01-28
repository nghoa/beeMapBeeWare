from flask_wtf import FlaskForm
from wtforms import Form, StringField, FloatField
from wtforms.validators import DataRequired, NumberRange
from flask import request


class SuggestionForm(Form):
    name = StringField('name', validators=[DataRequired()])
    latitude = FloatField("latitude", validators=[DataRequired(), NumberRange(-90,90)])
    longitude = FloatField("longitude", validators=[DataRequired(), NumberRange(-180,180)])
