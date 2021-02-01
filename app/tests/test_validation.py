from app.services.validation import SuggestionForm, ErrorMessage
import pytest
from app import create_app
from flask import request

"""
Tests validating sent form to save endpoint
Doesn't actually send request to save endpoint because 
it would require setting up fake database
"""

app = create_app()
app.config["TESTING"] = True

def test_normal():
    """
    Valid input, no errors
    """
    data = {"name": "Juha", "latitude": "22.4", "longitude": "12.34"}
    with app.test_request_context("/testing", data=data):
        form = SuggestionForm(request.form)
        assert form.validate()
        assert form.errors == {}

def test_missing():
    """
    Missing longitude
    """
    data = {"name": "Juha", "latitude": "22.4"}
    with app.test_request_context("/testing", data=data):
        form = SuggestionForm(request.form)
        assert not form.validate()
        assert form.errors == {"longitude": [ErrorMessage.REQUIRED]}

def test_zero_coercion():
    """
    Check that 0 is not interpreted as a missing value
    """
    data = {"name": "Juha", "latitude": "0", "longitude": "0"}
    with app.test_request_context("/testing", data=data):
        form = SuggestionForm(request.form)
        assert form.validate()
        assert form.errors == {}

def test_latitude_range():
    data = {"name": "Juha", "latitude": "13", "longitude": "14"}
    with app.test_request_context("/testing", data=data):
        form = SuggestionForm(request.form)
        assert form.validate()
        assert form.errors == {}

def test_latitude_range_off():
    data = {"name": "Juha", "latitude": "100.0", "longitude": "12.0"}
    with app.test_request_context("/testing", data=data):
        form = SuggestionForm(request.form)
        assert not form.validate()
        assert form.errors == {
            "latitude": [ErrorMessage.LATITUDE]
        }

def test_longitude_range_off():
    data = {"name": "Juha", "latitude": "12.0", "longitude": "200"}
    with app.test_request_context("/testing", data=data):
        form = SuggestionForm(request.form)
        assert not form.validate()
        assert form.errors == {
            "longitude": [ErrorMessage.LONGITUDE]
        }