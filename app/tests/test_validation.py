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
        assert form.errors == {"latitude": [ErrorMessage.INSIDE]}


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

def test_firstname_too_long():
    """
    Point outside Finland is not valid
    """
    data = {"firstname": "a"*40, "lastname": "bb", "longitude": "23", "latitude": "62", "email": "add@email.com"}
    with app.test_request_context("/testing", data=data):
        form = SuggestionForm(request.form)
        assert not form.validate()
        assert form.errors == {"firstname": [ErrorMessage.LENGTH_FIRSTNAME]}

def test_email_correct():
    """
    Test that correct email is valid
    """
    data = {"firstname": "a", "lastname": "bb", "longitude": "23", "latitude": "62", "email": "add@email.com"}
    with app.test_request_context("/testing", data=data):
        form = SuggestionForm(request.form)
        assert form.validate()
        assert form.errors == {}

def test_email_no_parts():
    """
    Test email missing @ and dot part
    """
    data = {"firstname": "a", "lastname": "bb", "longitude": "23", "latitude": "62", "email": "asdfdas"}
    with app.test_request_context("/testing", data=data):
        form = SuggestionForm(request.form)
        assert not form.validate()
        assert form.errors == {"email": [ErrorMessage.EMAIL_FORMAT]}

def test_email_no_dot():
    """
    Test missing dot part
    """
    data = {"firstname": "a", "lastname": "bb", "longitude": "23", "latitude": "62", "email": "asdfdas@fdfa"}
    with app.test_request_context("/testing", data=data):
        form = SuggestionForm(request.form)
        assert not form.validate()
        assert form.errors == {"email": [ErrorMessage.EMAIL_FORMAT]}


def test_email_no_():
    """
    Test missing beginning
    """
    data = {"firstname": "a", "lastname": "bb", "longitude": "23", "latitude": "62", "email": "@com.com"}
    with app.test_request_context("/testing", data=data):
        form = SuggestionForm(request.form)
        assert not form.validate()
        assert form.errors == {"email": [ErrorMessage.EMAIL_FORMAT]}

