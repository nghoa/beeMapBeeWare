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
#    print(f"Saved {task.key.name}: {task['LatLng']}")
    

def getLocations():
    client = datastore.Client()
    kind = "HiveLocation"
    locations = []
    for entity in client.query(kind=kind).fetch():
        print(entity["LatLng"])
        locations.append({
            "lat": entity["LatLng"].latitude,
            "lon": entity["LatLng"].longitude
        })
    return locations


def db_import_test() -> bool:
    """This is only for testing that loading this module works. If it doesn't, an 
    exception is thrown.

    Returns:
        bool: True
    """
    return True
