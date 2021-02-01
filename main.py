import os
from app import create_app

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
    start_app()

