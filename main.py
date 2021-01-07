from flask import Flask, render_template
import os
import logging

logger = logging.getLogger(__name__)
app = Flask(__name__)

@app.route('/')
def home():
    logger.debug("Front page requested.")
    return render_template('mymap.html')

if __name__ == '__main__':
    host = os.getenv("HOST", "127.0.0.1")
    port = os.getenv("PORT", "5000")

    logger.info(f"Starting buzzing service at {host}:{port}")
    app.run(host=host, port=port)
    logger.info(f"Stopping buzzing service at {host}:{port}")
