"""
Routing for main functionality
"""

import logging
from urllib.parse import urlencode

from . import map_blueprint
from app.services.database import get_suggestions, save_suggestion
from app.services.validation import SuggestionForm
from app.models.suggestion import Suggestion

from flask import session, redirect, url_for, escape, request, Response, render_template, make_response, jsonify
from flask_babel import gettext


logger = logging.getLogger()

@map_blueprint.route('/')
def home():
    """
    Map main page
    """
    form = SuggestionForm()
    
    return render_template('map.html', form = form)

@map_blueprint.route("/lang/<name>")
def change(name):
    """
    Change language
    load homepage again
    params:
        name: str short version of language name
    """
    if name in ["fi", "en"]:
        session["lang"] = name
    return redirect(url_for("map.home"))


@map_blueprint.route("/save", methods=["POST"])
def save():
    """
    Save received bee-village suggestion
    Request:
        http post request
            body: formdata (name, latitude, longitude)
    Response:
        json {"fieldname": ["errors"]}
    """
    form = SuggestionForm(request.form)
    if form.validate():
        suggestion = Suggestion.fromSuggestionForm(form)
        
        save_suggestion(suggestion)
        
        logger.debug("Bee-village suggestion saved.")
        
        status_code = 200
    else:
        logger.warn("Bee-village suggestion failed")
        status_code = 400 #bad request

    return jsonify(form.errors), status_code 
    


@map_blueprint.route("/locations", methods=["GET"])
def locations():
    """
    Response:
        json of suggestions
    """
    suggestions = get_suggestions()
    locations = []
    for suggestion in suggestions:
        locations.append({
            "latitude": suggestion.location.latitude,
            "longitude": suggestion.location.longitude,
            "confirmed": suggestion.confirmed
        })

    json_data = jsonify(locations)
    # make the response from json data requiderd by Flask. As HTTP code is used 200, OK
    resp = make_response(json_data, 200)
    resp.charset = "UTF-8"              # the charset of the response
    resp.mimetype = "application/json"  # the media type of the response

    return resp


