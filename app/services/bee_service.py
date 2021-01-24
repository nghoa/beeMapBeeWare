def doubleTime(x):
    """
    TODO: remove this function
    """
    return 2 * x

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

def save_suggestion(fields):
    """
    TODO: Saves the bee-village suggestion to database
    Params:
        fields: {"field name": "field value"}
    Returns:
        TODO: possible errors from database
    """
    pass


def getLocations():
    # TODO: get locations from database
    return [{"lat": 62, "lon": 27}, {"lat": 63, "lon": 26}]