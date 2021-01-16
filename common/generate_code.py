from os import environ
from uuid import uuid4

from utils.security.gen_token import EmailTokenGenerator


def gen_random_code():
    return uuid4().hex


def gen_confirmation_string_token_from_email(email):
    generator = EmailTokenGenerator(email=email.lower(), key=environ.get("SECRET_KEY"),
                                    salt=environ.get("EMAIL_CONFIRMATION_SALT")
                                    )
    return generator.gen_confirmation_email_token()