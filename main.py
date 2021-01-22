from flask import Flask, session, redirect, url_for, escape, request, Response, render_template, make_response, jsonify
import os

app = Flask(__name__)
app.debug = True

@app.route('/')
def home():
    return render_template('map.html')


def getLocations():
    # TODO: get locations from database
    return [{"lat": 62, "lon": 27}, {"lat": 63, "lon":26}]

@app.route("/locations",methods=["GET","POST"])
def locations():
    locations = getLocations()

    json_data = jsonify(locations)

    # make the response from json data requiderd by Flask. As HTTP code is used 200, OK
    resp = make_response(json_data, 200)
    resp.charset = "UTF-8"              # the charset of the response
    resp.mimetype = "application/json"  # the media type of the response

    return resp
    
def main():
    host = os.getenv("HOST", "127.0.0.1")
    port = os.getenv("PORT", "5000")

    app.run(host=host, port=port)

if __name__ == "__main__":
    main()