from datastore_entity import DatastoreEntity, EntityValue

class User(DatastoreEntity):
    Username = EntityValue(None)
    PasswordHash = EntityValue()
    __kind__ = "User"

    # call super class
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)


def test():
    user = User().find_by_value("Username", "admin", comparator="=")
    print(user[0])
    user[0].delete()
    # user.delete()

def validate_username():
    pass

def validate_email():
    pass

def set_password():
    pass

def check_password():
    pass

if __name__ == "__main__":
    test()