from flask import Flask

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('dev.cfg')
    register_blueprints(app)

    return app

def register_blueprints(app):
    # Since the application instance is now created, register each Blueprint
    # with the Flask application instance (app)
    from app.home import home_blueprint
    from app.map import map_blueprint
    from app.admin import admin_blueprint

    from app.services.auth import auth_blueprint
 
    app.register_blueprint(home_blueprint)
    app.register_blueprint(auth_blueprint)

    app.register_blueprint(map_blueprint, url_prefix='/map')
    app.register_blueprint(admin_blueprint, url_prefix='/admin')    