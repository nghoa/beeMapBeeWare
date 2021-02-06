from datastore_entity import DatastoreEntity, EntityValue
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# from app import login_manager

class User(DatastoreEntity, UserMixin):
    Username = EntityValue()
    PasswordHash = EntityValue()

    __kind__ = "User"

    def set_password(self, password):
        self.PasswordHash = generate_password_hash(password)
        return True

    def check_password(self, password):
        return check_password_hash(self.PasswordHash, password)

    # Overwrite
    def get_id(self):
        return self.Username
