"""
The home Blueprint handles the landing page for this application.
"""
from flask import Blueprint
map_blueprint = Blueprint('map', __name__, template_folder='templates')

from . import views