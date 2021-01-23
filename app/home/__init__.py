"""
The home Blueprint handles the landing page for this application.
"""
from flask import Blueprint
home_blueprint = Blueprint('home', __name__, template_folder='templates')

from . import views