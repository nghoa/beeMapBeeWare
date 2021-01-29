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
    

def getLocations():
    """
    Returns:
    {
        latitude: str, longitude: str, id: int
    }
    """
    client = datastore.Client()
    kind = "HiveLocation"
    
    locations = []
    for entity in client.query(kind=kind).fetch():
        latitude = entity["LatLng"].latitude
        longitude = entity["LatLng"].longitude

        locations.append({
            "longitude": longitude,
            "latitude": latitude
        })
    return locations
