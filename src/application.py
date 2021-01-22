from flask import Flask, session, redirect, url_for, escape, request, Response, render_template, make_response, jsonify
import os

app = Flask(__name__)

def doubleTime(x):
    """
    TODO: remove this function
    """
    return 2 * x

@app.route('/')
def home():
    return render_template('map.html')


def getLocations():
    # TODO: get locations from database
    return [{"lat": 62, "lon": 27}, {"lat": 63, "lon": 26}]

def get_fields(form, fields):
    """ 
    takes given fields from form
    Params:
        form: flask.request.form
        fields: list[(str,str)] list of field names and default values 
    Returns:
        dict[str, str] dictionary of field names and values 
    """
    #app.logger.debug(form.get("name"))
    return {name: form.get("name", default) for (name,default) in fields}

def validateForm(fields):
    """
    Checks that fields are valid
    TODO: write validations for form fields
    Params:
        fields: {"field name", "field value"}
    Returns:
        {"field name": "error message"}
    """
    errors = {}
    for k,v in fields.items():
        if not v:
            errors[k] = "Missing value"

    return errors

def parseSuggestion():
    """
    Parses json into fields
    """
    fields = request.get_json()
    #app.logger.debug(fields)

    return fields

def save_suggestion(fields):
    """
    TODO: Saves the bee-village suggestion to database
    Params:
        fields: {"field name": "field value"}
    Returns:
        TODO: possible errors from database
    """
    pass


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

    app.run(host=host, port=port, debug=True)


