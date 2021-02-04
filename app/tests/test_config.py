from app import create_app

app = create_app()
app.config["TESTING"] = True
# reads config from instance/instance_config.py
app.config.from_pyfile("instance_config.py")

def test_instance_config_exists():
    """
    Test that config has secret key and logging handler connection string
    """
    assert app.config.get("SECRET_KEY", None) is not None
    assert app.config.get("APPLICATIONINSIGHTS_CONNECTION_STRING", None) is not None
    