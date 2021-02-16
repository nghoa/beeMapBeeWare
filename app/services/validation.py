import re

from wtforms.validators import InputRequired, NumberRange, ValidationError, Length
from wtforms import Form, StringField, FloatField, HiddenField, SelectField
from wtforms.widgets import HiddenInput
from flask_babel import lazy_gettext
from shapely.geometry import Point, Polygon
from app.services.finland_polygon import finland_polygon_data


class ErrorMessage:
    REQUIRED = lazy_gettext("This field is required")
    INSIDE = lazy_gettext("Please select a location inside Finland")
    LENGTH_FIRSTNAME = lazy_gettext("Must be between 1 and 20 characters long")
    LENGTH_LASTNAME = lazy_gettext("Must be between 1 and 20 characters long")
    LENGTH_EMAIL = lazy_gettext("Must be between 1 and 254 characters long")
    EMAIL_FORMAT = lazy_gettext("Please enter valid email address")
    LENGTH_SUGGESTEE = lazy_gettext("Must be between 1 and 40 characters long")

def validate_email(form, field):
    """
    Check that email address is of correct format
    """
    emailstring = field.data
    if not re.match(r"[^@]+@[^@]+\.[^@]+", emailstring):
        raise ValidationError(ErrorMessage.EMAIL_FORMAT)


def validate_inside_Finland(form, field):
    """
    Check if given point is inside finland
    """
    try:
        lat = float(form.latitude.data)
        lng = float(form.longitude.data)
    except:
        raise ValidationError(ErrorMessage.INSIDE)
    point = Point(lng, lat)
    polygon = Polygon(finland_polygon_data)
    if not point.within(polygon):
        raise ValidationError(ErrorMessage.INSIDE)


class SuggestionForm(Form):
    firstname = StringField(lazy_gettext('firstname'), validators=[
        InputRequired(message=ErrorMessage.REQUIRED),
        Length(min=1, max=20, message=ErrorMessage.LENGTH_FIRSTNAME)
        ])

    lastname = StringField(lazy_gettext("lastname"), validators=[
        InputRequired(message=ErrorMessage.REQUIRED),
        Length(min=1, max=20, message=ErrorMessage.LENGTH_LASTNAME)])

    suggestee = StringField(lazy_gettext("name of the person or company who you wants to join"), validators=[
        InputRequired(message=ErrorMessage.REQUIRED),
        Length(min=1, max=40, message=ErrorMessage.LENGTH_SUGGESTEE)
    ])

    suggesteeType = SelectField(lazy_gettext("As"), choices=[
        ("0", lazy_gettext("Beekeeper")),
        ("1", lazy_gettext("Bee-friend")),
        ("2", lazy_gettext("sponsor"))
    ])

    latitude = FloatField(lazy_gettext("latitude"), validators=[
        validate_inside_Finland], widget=HiddenInput())

    longitude = FloatField(lazy_gettext("longitude"),widget = HiddenInput())

    email=StringField(lazy_gettext("email"), validators = [
                        InputRequired(message=ErrorMessage.REQUIRED),
                        Length(min=1, max=254, message=ErrorMessage.LENGTH_EMAIL),
                        validate_email])
