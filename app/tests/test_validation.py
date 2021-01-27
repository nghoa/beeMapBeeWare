from app.services.bee_service import validateForm

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
    result = validateForm({"name": "Juha", "latitude": "fdasdf", "longitude": "12.0"})
    assert "Expected a value of type 'float'" in result["latitude"]

def test_validate_one_missing():
    """
    longitude is missing
    """
    result = validateForm({"name": "Juha", "latitude": "12.0"})
    assert "Missing" in result["longitude"]

def test_validate_empty_value():
    """
    longitude has empty value
    """
    result = validateForm({"name": "Juha", "latitude": "12.0", "longitude": ""})
    assert "Missing" in result["longitude"]

def test_validate_empty_name():
    """
    Should return validation error if name is empty
    """
    result = validateForm({"name": "", "latitude": "12.0", "longitude": ""})
    assert "Missing" in result["name"]