import os
from app import create_app
from flask import Flask
# Middleware imports - the important ones
from opencensus.ext.flask.flask_middleware import FlaskMiddleware
from opencensus.trace.samplers import ProbabilitySampler
from opencensus.ext.azure.trace_exporter import AzureExporter

import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler

# Call the Application Factory function to construct a Flask application instance
# using the standard configuration defined in /instance/dev.cfg

app = create_app()
#reads app.config from instance/instance_config.py
#that has SECRET_KEY and APPLICATIONINSIGHTS_CONNECTION_STRING variables
app.config.from_pyfile("instance_config.py")

def _setup_azure_logging(logger: logging.Logger, app: Flask, connection_string: str):
    """Setup logging into Azure Application Insights.

    :param logger: Logging instance to assign azure opencensus stream handler.
    :param app: Flask app instance to assing azure opencensus handler.
    :param connection_string: Azure Application Insight connection string.
    """

    # Setup trace handler. Handles normal logging output:
    # >>> logger.info("Info message")
    azure_handler = AzureLogHandler(
        connection_string=connection_string
    )
    logger.addHandler(azure_handler)

    # Setup flask middleware, so pageview metrics are stored in azure.
    FlaskMiddleware(
        app,
        exporter=AzureExporter(connection_string=connection_string),
        sampler=ProbabilitySampler(rate=1.0),
    )

def start_app():
         
    host = os.getenv('HOST', '127.0.0.1')
    port = os.getenv('PORT', '5000')
    
    #load secret key from file, create this file yourself
    #https://gitlab.jyu.fi/startuplab/courses/tjts5901-continuous-software-engineering/beemaptemplate/-/blob/master/docs/adding-flask-config-file.md
    app.run(host=host, port=port) or logger.warning(f"Flask app {__name__} failed!")
    
if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    #log to local machine's stderr also
    logger.addHandler(logging.StreamHandler())

    # this comes from instance/instance_config.py
    _app_insight_connection = app.config.get("APPLICATIONINSIGHTS_CONNECTION_STRING")
    if _app_insight_connection:
        _setup_azure_logging(logger, app, _app_insight_connection)
    else:
        logger.warn("Missing azure application insight key. Logging to azure disabled.")

    start_app()

