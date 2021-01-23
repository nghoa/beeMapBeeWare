from . import home_blueprint
from app.services.test_service import test_servicez

@home_blueprint.route('/')
def hello():
    return 'Home page'
