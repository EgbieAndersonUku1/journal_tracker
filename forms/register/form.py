from wtforms import StringField, validators

from common.errors import EmailAdressAlreadyExists, InvalidUsernameFormat, UsernameAlreadyExists
from common.logger.logging import logger
from common.string_matcher import is_string_a_match

from forms.base_form import BaseEmailForm, BasePasswordForm
from models.users.user import User


class RegisterForm(BaseEmailForm, BasePasswordForm):
    username = StringField("Username", validators=[validators.DataRequired(), validators.Length(min=3, max=80)])

    def validate_username(form, field):

        reg_pattern = "^[a-zA-Z0-9_.-]+$"

        if User.find_by_username(username=field.data):
            logger.warning(f"An attempt was made to register with the {field.data.lower()} a username that already exists ")
            raise UsernameAlreadyExists("A users with that name already exists")

        if not is_string_a_match(reg_expression_pattern=reg_pattern, str_to_match=field.data):
            raise InvalidUsernameFormat("The username is invalid")

    def validate_email(form, field):

        if User.find_by_email(field.data):
            logger.warning(f"An attempt was made to register with the {field.data.lower()} a email that already exists ")
            raise EmailAdressAlreadyExists("The email already exists")
