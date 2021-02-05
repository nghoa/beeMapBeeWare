from datetime import datetime
from app.services.validation import SuggestionForm
from google.cloud.datastore.helpers import GeoPoint, Entity

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
    def fromSuggestionForm(cls, form: SuggestionForm):
        suggestion = Suggestion()
        suggestion.location = GeoPoint(form.latitude.data, form.longitude.data)
        suggestion.firstname = form.firstname.data
        suggestion.lastname = form.lastname.data
        
        suggestion.datetime = datetime.now()
        suggestion.confirmed = False
        
        return suggestion

    def populateEntity(self, entity) -> None:
        """
        puts fields from entity into object
        """
        entity["datetime"] = self.datetime
        entity["firstname"] = self.firstname
        entity["lastname"] = self.lastname
        entity["location"] = self.location
        entity["confirmed"] = self.confirmed
        entity["email"] = self.email

    @classmethod
    def fromEntity(cls, entity):
        suggestion = Suggestion()
        suggestion.id = entity.key.id
        suggestion.location = entity["location"]
        suggestion.firstname = entity["firstname"]
        suggestion.lastname = entity["lastname"]
        suggestion.datetime = entity["datetime"]
        suggestion.confirmed = entity["confirmed"]
        return suggestion        
