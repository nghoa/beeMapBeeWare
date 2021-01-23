"""
The admin Blueprint provides all admin-page func + view
"""
from flask import Blueprint
admin_blueprint = Blueprint('admin', __name__, template_folder='templates')

from . import views