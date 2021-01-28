import os
from google.type import latlng_pb2
from google.cloud.datastore.helpers import GeoPoint

from . import map_blueprint
from flask import session, redirect, url_for, escape, request, Response, render_template, make_response, jsonify
from app.services.database import getLocations, save_suggestion
from app.services.validation import SuggestionForm

@map_blueprint.route('/')
def home():
    form = SuggestionForm()
    return render_template('map.html', form = form)


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
        latitude = form.latitude.data
        longitude = form.longitude.data

        point = GeoPoint(latitude, longitude)
        save_suggestion(point)
        status_code = 200
    else:
        status_code = 400 #bad request

    return jsonify(form.errors), status_code 
    

@map_blueprint.route("/locations", methods=["GET"])
def locations():
    locations = getLocations()

    json_data = jsonify(locations)

    # make the response from json data requiderd by Flask. As HTTP code is used 200, OK
    resp = make_response(json_data, 200)
    resp.charset = "UTF-8"              # the charset of the response
    resp.mimetype = "application/json"  # the media type of the response

    return resp

