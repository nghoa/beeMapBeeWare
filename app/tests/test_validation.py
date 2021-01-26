from app.services.bee_service import validateForm
from app.services.bee_service import ErrorMessages

def test_validate_normal():
    """
    Valid input, no errors
    """
    actual = validateForm({"name": "Juha", "latitude": "22.4", "longitude": "12.34"})
    expected = {}
    assert actual == expected

def test_validate_not_float_parseable():
    """
    latitude isn't a float string
    """
    actual = validateForm({"name": "Juha", "latitude": "fdasdf", "longitude": "12.0"})
    expected = {"latitude": ErrorMessages.NOT_REAL}
    assert actual == expected

def test_validate_one_missing():
    """
    longitude is missing
    """
    actual = validateForm({"name": "Juha", "latitude": "12.0"})
    expected = {"longitude": ErrorMessages.MISSING}
    assert actual == expected

def test_validate_empty_value():
    """
    longitude has empty value
    """
    actual = validateForm({"name": "Juha", "latitude": "12.0", "longitude": ""})
    expected = {"longitude": ErrorMessages.MISSING}
    assert actual == expected
