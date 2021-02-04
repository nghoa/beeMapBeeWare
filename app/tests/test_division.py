import pytest
import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler
from app import create_app
from flask import Flask

app = create_app()
app.config["TESTING"] = True

import logging

logger = logging.getLogger()

def test_division_by_zero():
    """
        Test for division by zero
    """
    number = 2

    result = -1
    try:
        result = number / 0
    except ZeroDivisionError:
        logger.exception("Failed to divide by zero", exc_info=True)
    return f"{number} divided by zero is {result}"
