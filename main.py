import os
from app import create_app

# Call the Application Factory function to construct a Flask application instance
# using the standard configuration defined in /instance/dev.cfg

app = create_app()

def start_app():
    host = os.getenv('HOST', '127.0.0.1')
    port = os.getenv('PORT', '5000')

    app.run(host=host, port=port)

if __name__ == '__main__':
    start_app()

