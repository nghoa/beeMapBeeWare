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
    data = {"firstname": "aa", "lastname": "fdafda", "latitude": "62", "longitude": "23", "email": "add@email.com"}
    with app.test_request_context("/testing", data=data):
        form = SuggestionForm(request.form)
        assert form.validate()
        assert form.errors == {}

def test_missing():
    """
    Missing longitude
    """
    data = {"firstname": "aa", "lastname": "bb", "latitude": "62", "email": "add@email.com"}
    with app.test_request_context("/testing", data=data):
        form = SuggestionForm(request.form)
        assert not form.validate()
        assert form.errors == {"latitude": [ErrorMessage.INSIDE], "longitude": [ErrorMessage.REQUIRED]}


def test_inside():
    """
    Inside Finland is valid
    """
    data = {"firstname": "aa", "lastname": "bb", "longitude": "23", "latitude": "62", "email": "add@email.com"}
    with app.test_request_context("/testing", data=data):
        form = SuggestionForm(request.form)
        assert form.validate()
        assert form.errors == {}

def test_outside():
    """
    Point outside Finland is not valid
    """
    data = {"firstname": "aa", "lastname": "bb", "longitude": "16", "latitude": "63", "email": "add@email.com"}
    with app.test_request_context("/testing", data=data):
        form = SuggestionForm(request.form)
        assert not form.validate()
        assert form.errors == {"latitude": [ErrorMessage.INSIDE]}
