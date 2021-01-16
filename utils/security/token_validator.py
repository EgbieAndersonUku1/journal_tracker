from os import environ

from models.users.user import User
from utils.security.gen_token import EmailTokenGenerator


def is_user_confirmation_token_valid(user: "User", max_age_in_seconds: int = 86400) -> bool:
    """is_user_confirmation_token_valid(user: obj, max_age_in_seconds: int) returns bool

       A helper function that takes a user object and max_age_in_seconds and checks if the email
       confirmation token belonging to the user is valid. Returns True if it is
       or false otherwise

       :parameter
            :user: The user object containing the user's data
            :max_age_in_seconds: int: checks the expiry date for the token
    """
    tokenizer = EmailTokenGenerator(email=user.email.lower(), key=environ.get("SECRET_KEY"),
                                    salt=environ.get("EMAIL_CONFIRMATION_SALT"))
    return tokenizer.validate_confirmation_token(user.token, max_age=max_age_in_seconds)
