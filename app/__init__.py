from flask import Flask, session, request
from flask_babel import Babel

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    register_blueprints(app)

    register_localization(app)
    return app

def register_blueprints(app):
    # Since the application instance is now created, register each Blueprint
    # with the Flask application instance (app)
    from app.admin import admin_blueprint
    from app.map import map_blueprint

    from app.services.auth import auth_blueprint
 
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(map_blueprint)

    app.register_blueprint(admin_blueprint, url_prefix='/admin')    

def register_localization(app):
    """
    Configure babel with app
    """
    babel = Babel(app)

    def get_locale():
        """
        Decide what language to use
        """
        if "lang" in session:
            return session["lang"]
        #Decides the most suitable language option
        #fi=Finnish has higher priority
        lang = request.accept_languages.best_match(["fi", "en"])
        return lang

    babel.localeselector(get_locale)