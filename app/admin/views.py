from flask import render_template

from . import admin_blueprint

@admin_blueprint.route('/')
def profile():
    return render_template('profile.html')

