from wtforms import Form, StringField, FloatField
from wtforms.validators import InputRequired, NumberRange


class ErrorMessage:
    REQUIRED = "This field is required"
    LATITUDE = "Latitude has to be between -90 and 90"
    LONGITUDE = "Longitude has to be between -180 and 180"


class SuggestionForm(Form):
    firstname = StringField('firstname', validators=[
                        InputRequired(message=ErrorMessage.REQUIRED)])
    lastname = StringField("lastname", validators=[
                        InputRequired(message=ErrorMessage.REQUIRED)])
    latitude = FloatField("latitude", validators=[
                        InputRequired(message=ErrorMessage.REQUIRED), NumberRange(-90, 90, message=ErrorMessage.LATITUDE)])
    longitude = FloatField("longitude", validators=[
                        InputRequired(message=ErrorMessage.REQUIRED), NumberRange(-180, 180, message=ErrorMessage.LONGITUDE)])
    email = StringField("email", validators=[
                        InputRequired(message=ErrorMessage.REQUIRED)])