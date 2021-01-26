class ErrorMessages:
    MISSING = "Missing value"
    NOT_REAL = "Must be real number"


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

def validateValue(fields, field, isFloat = False):
    if not field in fields:
        return ErrorMessages.MISSING
    if not fields[field]:
        return ErrorMessages.MISSING
    if isFloat:
        try:
            float(fields[field])
        except:
            return ErrorMessages.NOT_REAL
    return None

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
    requiredFields = [("name", False), ("latitude", True), ("longitude", True)]
    for field, isFloat in requiredFields:
        error = validateValue(fields, field, isFloat)
        if error is not None:
            errors[field] = error
    
    return errors
