from google.cloud import datastore


def save_suggestion(location):
    """
        Saves the bee-village suggestion to database
    Params:
        location: GeoPoint(latitude, longitude)
    Returns:
        TODO: possible errors from database 
    """
    client = datastore.Client()

    kind = "HiveLocation"
    task_key = client.key(kind)
    task = datastore.Entity(key=task_key)
    task["LatLng"] = location
    client.put(task)
    
def delete_suggestion(id):
    """
    Tries to delete entity based on it's id
    if it doesn't exist, does nothing
    """
    client = datastore.Client()

    kind = "HiveLocation"
    key = client.key(kind, id)
    client.delete(key)

def getLocations():
    """
    Returns:
        {
            latitude: float, 
            longitude: float, 
            id: int
        }
    """
    client = datastore.Client()
    kind = "HiveLocation"
    
    locations = []
    for entity in client.query(kind=kind).fetch():
        latitude = entity["LatLng"].latitude
        longitude = entity["LatLng"].longitude
        id = entity.key.id
        locations.append({
            "longitude": longitude,
            "latitude": latitude,
            "id": id
        })
    return locations
