import logging
from google.cloud import datastore
from werkzeug.security import generate_password_hash

import logging
from app.models.suggestion import Suggestion
from typing import List

logger = logging.getLogger()


def save_suggestion(suggestion: Suggestion):
    """
    Saves the bee-village suggestion to database
    """
    client = datastore.Client()

    kind = "Suggestion"
    k = client.key(kind)
    entity = datastore.Entity(key=k)
    suggestion.populateEntity(entity)

    logger.debug(f"Saved location {suggestion}")

    client.put(entity)
    
def delete_suggestion(id):
    """
    Tries to delete entity based on it's id
    if it doesn't exist, does nothing
    """
    client = datastore.Client()

    kind = "Suggestion"
    key = client.key(kind, id)

    logger.debug(f"Deleted {key}.")
    client.delete(key)

def get_suggestions():
    client = datastore.Client()
    kind = "Suggestion"
    
    suggestions = []
    for entity in client.query(kind=kind).fetch():
        suggestion = Suggestion.fromEntity(entity)
        suggestions.append(suggestion)
    
    hiveCount = len(suggestions)

    if hiveCount > 0:
        logging.debug(f"Found {hiveCount} locations")
    else:
        logging.warn("No hive locations found")
        
    return suggestions


def update_suggestion(id):
    pass



def get_user(username):
    kind = "User"
    client = datastore.Client()
    query = client.query(kind=kind)
    query_iter = query.add_filter('Username', '=', username).fetch()
    user_entity = list(query_iter)

    logging.debug(f"Found user {user_entity}")
    return(user_entity)


if __name__ == "__main__":
    pass