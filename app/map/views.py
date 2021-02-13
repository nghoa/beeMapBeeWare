"""
Routing for main functionality
"""

import logging
from ipaddress import ip_address

from . import map_blueprint
from app.services.database import get_suggestions, save_suggestion, get_recent_ip_addresses, delete_recent_ips, save_ip
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
        200 {} valid suggestion
        400 {} if ip address parsing fails
        400 {"fieldname": ["errors"]} if not valid suggestion
        429 {} if ip has made too many suggestions recently
    """

    form = SuggestionForm(request.form)
    if form.validate():
        try:
            ip = request.remote_addr
            ip = ip_address(ip)
        except:
            return jsonify({}), 400 #bad request

        recent_ips = get_recent_ip_addresses()
        ip_found_count = 0
        for recent_ip in recent_ips:
            if recent_ip == ip:
                ip_found_count += 1
        # how many suggestions one user can make out of the most recent 1000
        max_by_one = 10
        # maximum number of recent ips to save to datastore
        # after limit has been reached all the old ones are removed
        # since deletion is blocking operation it's not wise to make this very large
        # as user would have to wait a long time for the response to return
        max_in_datastore = 1000
        
        if len(recent_ips) > max_in_datastore:
            delete_recent_ips()

        if ip_found_count > max_by_one:
            return jsonify({}), 429 #too many requests

        suggestion = Suggestion.fromSuggestionForm(form)
        
        save_suggestion(suggestion)
        
        save_ip(ip)
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


