from flask import Flask

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    register_blueprints(app)

    return app

def register_blueprints(app):
    # Since the application instance is now created, register each Blueprint
    # with the Flask application instance (app)
    from app.admin import admin_blueprint
    from app.map import map_blueprint
 
    app.register_blueprint(map_blueprint)

    app.register_blueprint(admin_blueprint, url_prefix='/admin')    