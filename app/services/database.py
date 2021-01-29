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


# user models separated by file?

def getUser():
    client = datastore.Client()
    kind = "User"
    for entity in client.query(kind=kind).fetch():
        password = entity["Password"]
        password_hash = entity["PasswordHash"]
        username = entity["Username"]
        print(password)
        print(password_hash)
        print(username)


if __name__ == "__main__":
    getUser()