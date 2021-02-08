from wtforms import Form, StringField, FloatField
from wtforms.validators import InputRequired, NumberRange, ValidationError
from flask_babel import lazy_gettext
from shapely.geometry import Point, Polygon
from app.services.finland_polygon import finland_polygon_data


class ErrorMessage:
    REQUIRED = lazy_gettext("This field is required")
    INSIDE = lazy_gettext("Please select a location inside Finland")

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
        InputRequired(message=ErrorMessage.REQUIRED)])
    lastname = StringField(lazy_gettext("lastname"), validators=[
        InputRequired(message=ErrorMessage.REQUIRED)])
    latitude = FloatField(lazy_gettext("latitude"), validators=[
        InputRequired(message=ErrorMessage.REQUIRED), 
        validate_inside_Finland])
    longitude = FloatField(lazy_gettext("longitude"), validators=[
        InputRequired(message=ErrorMessage.REQUIRED)])
    email = StringField(lazy_gettext("email"), validators=[
                        InputRequired(message=ErrorMessage.REQUIRED)])
