from flask import Flask
from flask_login import LoginManager

from secrets import token_urlsafe
from app.admin.models import User

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    # TODO: establish shared variable file for teammember
    app.secret_key = token_urlsafe(16)

    register_blueprints(app)

    # fast login manager implement
    login_manager = LoginManager(app)
    login_manager.login_view = 'admin.login'
    @login_manager.user_loader
    def load_user(username):    
        return User().get_obj('Username', username)

    return app

def register_blueprints(app):
    # Since the application instance is now created, register each Blueprint
    # with the Flask application instance (app)
    from app.admin import admin_blueprint
    from app.map import map_blueprint
 
    app.register_blueprint(map_blueprint)

    app.register_blueprint(admin_blueprint, url_prefix='/admin')    