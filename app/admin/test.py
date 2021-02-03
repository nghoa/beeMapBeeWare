from datastore_entity import DatastoreEntity, EntityValue
from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash

import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Azure loghandler.
connection_string = "InstrumentationKey=bfe6d9a0-78dc-40fb-a307-b0d8c97bc266;IngestionEndpoint=https://northeurope-0.in.applicationinsights.azure.com/"
logger.addHandler(AzureLogHandler(connection_string=connection_string))

class User(DatastoreEntity, UserMixin):
    Username = EntityValue()
    PasswordHash = EntityValue()

    __kind__ = "User"

    def set_password(self, password):
        self.PasswordHash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.PasswordHash, password)

# @login_manager.user_loader
def load_user(username):
    return User().get_obj('Username', username)


if __name__ == '__main__':
    user = User().get_obj('Username', "admin")

    test = user.check_password("admin")
    logger.debug("User: {test}")
    print(test)
