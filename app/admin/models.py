from flask_login import UserMixin
from datastore_entity import DatastoreEntity, EntityValue
from werkzeug.security import generate_password_hash, check_password_hash


class User(DatastoreEntity, UserMixin):
    username = EntityValue(None)
    password_hash = EntityValue(None)

    def set_password(self, password):
        self.password_hash = ""