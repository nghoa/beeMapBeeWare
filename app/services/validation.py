from flask_wtf import FlaskForm
from wtforms import Form, StringField, FloatField
from wtforms.validators import InputRequired, NumberRange
from flask import request
from enum import Enum
from typing import Optional, Dict


class ErrorMessage:
    REQUIRED = "This field is required"
    LATITUDE = "Latitude has to between -90 and 90"
    LONGITUDE = "Longitude has to be between -180 and 180"


class SuggestionForm(Form):
    name = StringField('name', validators=[
                       InputRequired(message=ErrorMessage.REQUIRED)])
    latitude = FloatField("latitude", validators=[
                          InputRequired(message=ErrorMessage.REQUIRED), NumberRange(-90, 90, message=ErrorMessage.LATITUDE)])
    longitude = FloatField("longitude", validators=[
                           InputRequired(message=ErrorMessage.REQUIRED), NumberRange(-180, 180, message=ErrorMessage.LONGITUDE)])
