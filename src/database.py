from google.cloud import datastore

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
    client = datastore.Client()
    kind = "HiveLocation"
    locations = []
    for entity in client.query(kind=kind).fetch():
        locations.append({
            "lat": entity["LatLng"].latitude,
            "lon": entity["LatLng"].longitude
        })
    return locations
    