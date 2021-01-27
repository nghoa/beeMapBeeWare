from enum import Enum
from typing import Optional, Dict

ValidationError = str  # use strings to represent validation errors at least for now


class FieldType(Enum):
    """
    Form field types that are used for validating fields' values.
    Their values (FieldType.*.value) should be understandable.
    """
    FLOAT = "float"
    NONEMPTY_STRING = "nonempty string"
    EMAIL = "email"


class ErrorMessage:
    """
    Contains methods for creating error messages.
    """
    @staticmethod
    def missing_value() -> ValidationError:
        """
        Return this if field's value is missing (None).

        Returns:
            ValidationError: message describing the validation error
        """
        return "Missing value"

    @staticmethod
    def type_mismatch(field_type: FieldType, value) -> ValidationError:
        """
        Return this if the field's actual type doesn't match the intended.

        Args:
            field_type (FieldType): that was expected
            value ([type]): which was isn't of the expected type

        Returns:
            ValidationError: message describing the validation error
        """
        return f"Expected a value of type '{field_type.value}', was {value}"


def get_fields(form, fields):
    """ 
    takes given fields from form
    Params:
        form: flask.request.form
        fields: list[(str,str)] list of field names and default values 
    Returns:
        dict[str, str] dictionary of field names and values 
    """
    # app.logger.debug(form.get("name"))
    return {name: form.get("name", default) for (name, default) in fields}


def validateValue(fields, field: str, field_type: FieldType) -> Optional[ValidationError]:
    """
    Validate a value in fields with validation rules for given field type.

    Args:
        fields: fields from form
        field (str): field to be validated
        field_type (FieldType): type of field

    Returns:
        Optional[ValidationError]: None if no error. Validation error if value is 
        invalid.
    """
    value = fields.get(field, None)
    if not value:
        return ErrorMessage.missing_value()
    if field_type == FieldType.FLOAT:
        try:
            float(value)
        except:
            return ErrorMessage.type_mismatch(FieldType.FLOAT, value)
    elif field_type == FieldType.NONEMPTY_STRING:
        if value != "":
            return None
        else:
            return ErrorMessage.type_mismatch(FieldType.NONEMPTY_STRING, value)
    return None


def validateForm(fields) -> Dict[str, ValidationError]:
    """
    Validate form fields' contents. Each field gets their own validation error message
    if any.
    Params:
        fields: {"field name", "field value"}
    Returns:
        {"field name": "error message"}
    """
    errors = {}
    requiredFields = [
        ("name", FieldType.NONEMPTY_STRING),
        ("latitude", FieldType.FLOAT),
        ("longitude", FieldType.FLOAT),
    ]

    for field, isFloat in requiredFields:
        error = validateValue(fields, field, isFloat)
        if error is not None:
            errors[field] = error

    return errors
