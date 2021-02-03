import os
from app import create_app

# Middleware imports - the important ones
from opencensus.ext.flask.flask_middleware import FlaskMiddleware
from opencensus.trace.samplers import ProbabilitySampler
from opencensus.ext.azure.trace_exporter import AzureExporter

# Call the Application Factory function to construct a Flask application instance
# using the standard configuration defined in /instance/dev.cfg

app = create_app()
app.config.from_pyfile("instance_config.py")

def start_app():
    
    host = os.getenv('HOST', '127.0.0.1')
    port = os.getenv('PORT', '5000')
    
    #load secret key from file, create this file yourself
    #https://gitlab.jyu.fi/startuplab/courses/tjts5901-continuous-software-engineering/beemaptemplate/-/blob/master/docs/adding-flask-config-file.md
    app.run(host=host, port=port)
    
if __name__ == '__main__':

    connection_string = "InstrumentationKey=bfe6d9a0-78dc-40fb-a307-b0d8c97bc266;IngestionEndpoint=https://northeurope-0.in.applicationinsights.azure.com/"

    FlaskMiddleware(
    app,
    exporter=AzureExporter(connection_string=connection_string),
    sampler=ProbabilitySampler(rate=1.0),
    )

    start_app()

