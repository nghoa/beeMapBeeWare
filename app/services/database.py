"""
Datastore access functionality
"""

import logging
from ipaddress import ip_address

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
    Params:
        id: int datastore id for suggestion to delete
    """
    client = datastore.Client()

    kind = "Suggestion"
    key = client.key(kind, id)

    logger.debug(f"Deleted {key}.")
    client.delete(key)

def get_suggestions():
    """
    Fetches all Suggestions from datastore
    Returns:
        List[Suggestion]
    """
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


"""
    Update the status of the suggested beehive
    - property "confirmed" under Suggestion entity
"""
def update_suggestion_status(id, status):
    client = datastore.Client()
    kind = "Suggestion"
    key = client.key(kind, id)
    entity = client.get(key)
    entity.update({'confirmed': status})
    client.put(entity)

def get_recent_ip_addresses():
    """
    Get list of ip addresses from datastore
    """
    client = datastore.Client()
    kind = "RecentIp"
    
    ips = []
    for entity in client.query(kind=kind).fetch():
        try:
            ip = entity["ip"]
            ip = ip_address(ip)
            ips.append(ip)
        except:
            pass

    return ips


def _get_ip_keys():
    """
    Ip keys
    """
    client = datastore.Client()
    kind = "RecentIp"

    ipkeys = []
    for entity in client.query(kind = kind).fetch():
        ipkeys.append(entity.key)
    return ipkeys

def save_ip(ip):
    """
    Saves this ip to recent ips
    """
    client = datastore.Client()
    kind = "RecentIp"
    k = client.key(kind)
    entity = datastore.Entity(key=k)
    entity["ip"] = str(ip)

    client.put(entity)


def delete_recent_ips():
    """
    Delete all ips in datastore
    """
    client = datastore.Client()
    keys = _get_ip_keys()
    client.delete_multi(keys)
    

def get_user(username):
    kind = "User"
    client = datastore.Client()
    query = client.query(kind=kind)
    query_iter = query.add_filter('Username', '=', username).fetch()
    user_entity = list(query_iter)

    logging.debug(f"Found user {user_entity}")
    return(user_entity)


if __name__ == "__main__":
    # id = 5629978607616000
    # update_suggestion_status(id, True)
    pass