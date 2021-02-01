from google.cloud import datastore
from werkzeug.security import generate_password_hash


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



# user models separated by file?
def get_all_users():
    kind = "User"
    client = datastore.Client()
    for entity in client.query(kind=kind).fetch():
        print(entity)


def get_user(username):
    kind = "User"
    client = datastore.Client()
    query = client.query(kind=kind)
    query_iter = query.add_filter('Username', '=', username).fetch()
    user_entity = list(query_iter)
    return(user_entity)


def create_admin_user(username, password):
    kind = "User"
    client = datastore.Client()
    hash = generate_password_hash(password)
    print(hash)

if __name__ == "__main__":
    pass