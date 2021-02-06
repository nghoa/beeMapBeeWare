from datetime import datetime
from google.cloud.datastore.helpers import GeoPoint, Entity

from openpyxl import Workbook

class Suggestion:
    """
    Bee-village location suggestion
    id: int, 
    datetime: datetime, 
    firstname: str, 
    lastname: str, 
    location: GeoPoint
    confirmed: bool, 
    email: str
    """

    def __init__(self):
        self.id = None
        self.datetime = None
        self.firstname = None
        self.lastname = None
        self.location = None
        self.confirmed = None
        self.email = None

    @classmethod
    def fromSuggestionForm(cls, form):
        """
        Creates suggestion from SuggestionForm object
        """
        suggestion = Suggestion()
        suggestion.datetime = datetime.now()
        suggestion.firstname = form.firstname.data
        suggestion.lastname = form.lastname.data
        suggestion.location = GeoPoint(form.latitude.data, form.longitude.data)
        suggestion.confirmed = False
        suggestion.email = form.email.data

        return suggestion

    def populateEntity(self, entity) -> None:
        """
        puts fields from entity into object
        don't read id as it doesn't exists yet
        """
        entity["datetime"] = self.datetime
        entity["firstname"] = self.firstname
        entity["lastname"] = self.lastname
        entity["location"] = self.location
        entity["confirmed"] = self.confirmed
        entity["email"] = self.email

    @classmethod
    def fromEntity(cls, entity):
        """
        Creates suggestion from datastore entity
        """
        suggestion = Suggestion()
        suggestion.id = entity.key.id
        suggestion.datetime = entity["datetime"]
        suggestion.firstname = entity["firstname"]
        suggestion.lastname = entity["lastname"]
        suggestion.location = entity["location"]
        suggestion.confirmed = entity["confirmed"]
        suggestion.email = entity["email"]
        return suggestion

    @staticmethod
    def suggestions_to_excel(suggestions):
        """
        Transforms list of suggestions into an excel workbook
        with header row from attribute names, makes location into two columns
        latitude, longitude
        """
        wb = Workbook()
        #first worksheet, created automatically
        ws = wb.active

        #header row
        ws.append(["id", "datetime", "firstname", "lastname", "latitude", "longitude", "confirmed", "email"])
        for suggestion in suggestions:
            row = [
                suggestion.id,
                suggestion.datetime,
                suggestion.firstname,
                suggestion.lastname,
                suggestion.location.latitude,
                suggestion.location.longitude,
                suggestion.confirmed,
                suggestion.email
            ]
            ws.append(row)

        #make datetime column wider so it shows nicely in excel
        ws.column_dimensions["B"].width = 22

        return wb