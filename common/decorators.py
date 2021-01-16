from datetime import datetime
from os import environ

from itsdangerous import SignatureExpired
from flask import abort, flash, session, url_for
from functools import wraps

from common.emails.send_emails.send_email import resend_user_expired_token_link
from common.logger.logging import logger
from models.users.user import User
from utils.security.secure_redirect import secure_redirect_or_403
from utils.security.token_validator import is_user_confirmation_token_valid


def admin_required(f):
    @wraps(f)
    def is_admin(*args, **kwargs):
        email = session["email"]
        if email != environ.get("ADMIN_EMAIL"):
            logger.critical(f"The user with the email <{email}> attempted to access a protected area")
            abort(403)
        return f(*args, **kwargs)
    return is_admin


def is_logged_in(f):
    @wraps(f)
    def is_logged_in(*args, **kwargs):

        if session.get("username"):
            return secure_redirect_or_403(url_for('home_app.landing_page'))
        return f(*args, **kwargs)
    return is_logged_in


def login_required(f):
    @wraps(f)
    def is_user_logged_in(*args, **kwargs):

        if session.get("username") is None:
            return secure_redirect_or_403(url_for('home_app.home'))
        return f(*args, **kwargs)
    return is_user_logged_in


def is_confirmation_token_valid(f):
    @wraps(f)
    def validate_token(*args, **kwargs):

        username = kwargs["username"]
        user = User.find_by_username(username)

        if not user:
            abort(404)
        elif user.token is None:
            flash("There is no token to validate", "info")
        elif user.token != kwargs["token"]:
            logger.warning(f"The user {user.username.title()} tried to validate with an invalid token")
            abort(400)
        else:
            try:
                is_user_confirmation_token_valid(user)

            except SignatureExpired:

                flash("The confirmation token has has expired", "info")
                flash("A new confirmation token has be re-sent to your email address. Check your inbox or spam")

                logger.warning(f"The token for the user {user.username.title()} has expired. A new one was sent to the user")

                resend_user_expired_token_link(user)
                return secure_redirect_or_403(url_for('home_app.landing_page'))
            else:
                user.email_confirmed = True
                user.email_confirmed_on = datetime.now()
                user.token = None
                user.save()
                flash("You have successful confirmed your email and your account is now ready to by used. You can now login", "success")

        return f(*args, **kwargs)

    return validate_token



