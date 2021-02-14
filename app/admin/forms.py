from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.admin.models import User

from flask_babel import lazy_gettext

class LoginForm(FlaskForm):
    username = StringField(lazy_gettext('Username'), validators=[DataRequired()])
    password = PasswordField(lazy_gettext('Password'), validators=[DataRequired()])
    remember_me = BooleanField(lazy_gettext('Remember Me'))
    submit = SubmitField(lazy_gettext('Login'))


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(lazy_gettext('Old Password'), validators=[DataRequired()])
    new_password = PasswordField(lazy_gettext('New Password'), validators=[DataRequired()])
    submit = SubmitField(lazy_gettext('Change Password'))