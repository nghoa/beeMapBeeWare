from . import home_blueprint

@home_blueprint.route('/')
def hello():
    return 'Home page'
