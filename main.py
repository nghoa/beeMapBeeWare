import os

from flask import Flask, session, redirect, url_for, escape, request, Response, render_template, make_response, jsonify

from src.bee_service import get_fields, validateForm
from src.database import getLocations, save_suggestion

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('map.html')


def parseSuggestion():
    """
    Parses json into fields
    """
    fields = request.get_json()
    #app.logger.debug(fields)

    return fields


@app.route("/save", methods=["POST"])
def save():
    """
    Save received bee-village suggestion
    Response:
        message telling if the suggestion was valid
    """
    fields = parseSuggestion()

    errors = validateForm(fields)
    if len(errors) == 0:
        save_suggestion(fields)
        status_code = 200
    else:
        status_code = 400 #bad request
    
    return jsonify(errors), status_code 
    

@app.route("/locations", methods=["GET", "POST"])
def locations():
    locations = getLocations()

    json_data = jsonify(locations)

    # make the response from json data requiderd by Flask. As HTTP code is used 200, OK
    resp = make_response(json_data, 200)
    resp.charset = "UTF-8"              # the charset of the response
    resp.mimetype = "application/json"  # the media type of the response

    return resp


def start_app():
    host = os.getenv("HOST", "127.0.0.1")
    port = os.getenv("PORT", "5000")

    app.run(host=host, port=port)


if __name__ == "__main__":
    start_app()

