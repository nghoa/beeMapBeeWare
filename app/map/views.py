import os
from google.type import latlng_pb2
from google.cloud.datastore.helpers import GeoPoint

from . import map_blueprint
from flask import session, redirect, url_for, escape, request, Response, render_template, make_response, jsonify
from app.services.bee_service import get_fields, validateForm
from app.services.database import getLocations, save_suggestion


@map_blueprint.route('/')
def home():
    return render_template('map.html')


def parseSuggestion():
    """
    Parses json into fields
    """
    fields = request.get_json()
    #app.logger.debug(fields)

    return fields


@map_blueprint.route("/save", methods=["POST","GET"])
def save():
    """
    Save received bee-village suggestion
    Response:
        message telling if the suggestion was valid
    """
    fields = parseSuggestion()

    # get the latitude and longitude from the form
    location = fields["location"].split(" ")

    # l = GeoPoint(latitude, longitude)
    l = GeoPoint(float(location[1]), float(location[3]))
    
    errors = validateForm(fields)
    if len(errors) == 0:
        save_suggestion(l)
        status_code = 200
    else:
        status_code = 400 #bad request
    
    return jsonify(errors), status_code 
    

@map_blueprint.route("/locations", methods=["GET", "POST"])
def locations():
    locations = getLocations()

    json_data = jsonify(locations)

    # make the response from json data requiderd by Flask. As HTTP code is used 200, OK
    resp = make_response(json_data, 200)
    resp.charset = "UTF-8"              # the charset of the response
    resp.mimetype = "application/json"  # the media type of the response

    return resp

