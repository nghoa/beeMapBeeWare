import os
from google.type import latlng_pb2
from google.cloud.datastore.helpers import GeoPoint

from . import map_blueprint
from flask import session, redirect, url_for, escape, request, Response, render_template, make_response, jsonify, send_file, after_this_request
from app.services.database import get_suggestions, save_suggestion, delete_suggestion
from app.services.validation import SuggestionForm
from app.models.suggestion import Suggestion

from tempfile import NamedTemporaryFile

from flask_babel import gettext
from opencensus.ext.azure.log_exporter import AzureLogHandler   # I guess this is isn't necessary..

import logging

logger = logging.getLogger()

@map_blueprint.route('/')
def home():
    form = SuggestionForm()
    return render_template('map.html', form = form)

@map_blueprint.route("/lang/<name>")
def change(name):
    """
    Change language
    load homepage again
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
    
@map_blueprint.route("/delete/<int:id>", methods=["GET"])
def delete(id):
    """
    Deletes suggestion from database with given id
    if it exists
    Params:
        id: entity id, gets converted to int
    """

    logger.debug("Bee-village deleted.")

    delete_suggestion(id)
    return "ok", 200

@map_blueprint.route("/locations", methods=["GET"])
def locations():
    suggestions = get_suggestions()
    locations = []
    for suggestion in suggestions:
        locations.append({
            "latitude": suggestion.location.latitude,
            "longitude": suggestion.location.longitude,
            "id": suggestion.id,
            "confirmed": suggestion.confirmed
        })

    json_data = jsonify(locations)
    # make the response from json data requiderd by Flask. As HTTP code is used 200, OK
    resp = make_response(json_data, 200)
    resp.charset = "UTF-8"              # the charset of the response
    resp.mimetype = "application/json"  # the media type of the response

    return resp


""" @map_blueprint.route("/export")
def export():
    suggestions = get_suggestions()
    wb = Suggestion.suggestions_to_excel(suggestions)
    ws = wb.active
    def generate():
        for row in ws:
              yield ",".join([str(cell.value) for cell in row]) + "\n"    
    return Response(generate(), mimetype="text/csv") """

@map_blueprint.route("/export")
def export():
    suggestions = get_suggestions()
    wb = Suggestion.suggestions_to_excel(suggestions)
    with NamedTemporaryFile(dir=".", suffix=".xlsx") as tmp:
        wb.save(tmp)
        tmp.seek(0)
        stream = tmp.read()
    
    return Response(stream, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")