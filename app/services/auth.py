from werkzeug.security import generate_password_hash, check_password_hash

# check pw_hash => generate authentication
def authenticate_admin(hash, password):
    check_password_hash(hash, password)
    # >>> True | False