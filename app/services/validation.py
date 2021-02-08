from wtforms import Form, StringField, FloatField, HiddenField
from wtforms.widgets import HiddenInput
from wtforms.validators import InputRequired, NumberRange
from flask_babel import lazy_gettext

class ErrorMessage:
    REQUIRED = lazy_gettext("This field is required")
    LATITUDE = lazy_gettext("Latitude has to be between -90 and 90")
    LONGITUDE = lazy_gettext("Longitude has to be between -180 and 180")


class SuggestionForm(Form):
    firstname = StringField(lazy_gettext('firstname'), validators=[
                        InputRequired(message=ErrorMessage.REQUIRED)])
    lastname = StringField(lazy_gettext("lastname"), validators=[
                        InputRequired(message=ErrorMessage.REQUIRED)])
    latitude = FloatField(
        lazy_gettext("latitude"),
        validators=[
            InputRequired(message=ErrorMessage.REQUIRED), 
            NumberRange(-90, 90, message=ErrorMessage.LATITUDE)
        ],
        widget=HiddenInput())

    longitude = FloatField(
        lazy_gettext("longitude"), 
        validators=[
            InputRequired(message=ErrorMessage.REQUIRED),
            NumberRange(-180, 180, message=ErrorMessage.LONGITUDE)
        ],
        widget=HiddenInput())

    email = StringField(lazy_gettext("email"), validators=[
                        InputRequired(message=ErrorMessage.REQUIRED)])