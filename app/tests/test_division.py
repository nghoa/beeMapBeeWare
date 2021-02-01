import pytest
import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler
from app import create_app
from flask import Flask

app = create_app()
app.config["TESTING"] = True

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Azure loghandler.
connection_string = "InstrumentationKey=bfe6d9a0-78dc-40fb-a307-b0d8c97bc266;IngestionEndpoint=https://northeurope-0.in.applicationinsights.azure.com/"
logger.addHandler(AzureLogHandler(connection_string=connection_string))

@app.route("/_divide_by_zero/<int:number>", methods=["GET"])
def division_by_zero(number: int):

    """
        Test for division by zero
    """
    result = -1
    try:
        result = number / 0
    except ZeroDivisionError:
        logger.exception("Failed to divide by zero", exc_info=True)
    return f"{number} divided by zero is {result}"
