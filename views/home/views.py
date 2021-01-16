from datetime import datetime
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from os import environ

from common.emails.send_emails.send_email import email_user_confirmation_email_link, send_user_contact_message
from common.emails.send_emails.send_email import email_notification_to_owner_about_new_user_registration
from common.decorators import is_logged_in, login_required
from common.decorators import is_confirmation_token_valid
from common.errors import FailedToSendEmail
from common.generate_code import gen_confirmation_string_token_from_email
from common.logger.logging import logger
from forms.contact_us.form import ContactForm
from forms.login.form import LoginForm
from forms.register.form import RegisterForm
from models.users.user import User
from utils.security.passwordImplementer import PasswordImplementer
from utils.security.secure_redirect import secure_redirect_or_403

home_app = Blueprint("home_app", __name__)


@home_app.route("/contact", methods=["GET", "POST"])
def contact_us() -> "render_template('index.html')":

    form = ContactForm()

    if request.method == "POST" and form.validate_on_submit():
        send_user_contact_message(email=form.email.data.strip(),
                                  first_name=form.first_name.data,
                                  message=form.message.data,
                                  surname=form.surname.data,

                                  )
        flash("Your message has been send to the administrator", "success")
        return secure_redirect_or_403(url_for("home_app.landing_page"))

    return render_template("index.html", contact_form=form, login_form=LoginForm(), register_form=RegisterForm())


@home_app.route("/<username>/confirm/<token>")
@is_confirmation_token_valid
def confirm(username: str, token: str) -> "render_template(url_for('account_app.account_setup'))": # Username and token will be send through to the decorator
    """confirm(username: str, token: str) -> redirects to a template

       Takes a username and a token and checks if the token belong to the
       is valid.

       :parameter
            :username: Takes a string in the form a username
            :token: The user token that will be verified by the server

    """
    return redirect(url_for("account_app.account_setup", username=username))


@home_app.route("/dashboard")
@login_required
def dashboard() -> "render_template('dashboard/dashboard.html')":
    """The browse page enables the user to access all the features of the application"""
    return render_template("dashboard/dashboard.html", ADMIN_EMAIL=environ.get("ADMIN_EMAIL"), login_form=LoginForm())


@home_app.route("/")
@home_app.route("/register", methods=["GET", "POST"])
@is_logged_in
def home() -> "render_template('index.html')":

    form = RegisterForm()

    if request.method == "POST":

        if form.validate_on_submit():

            email, username = form.email.data.lower().strip(), form.username.data.strip().lower()
            token = gen_confirmation_string_token_from_email(email)
            try:
                email_user_confirmation_email_link(username=username, email=email, token=token)
            except FailedToSendEmail:
                logger.critical(f"Failed to send a confirmation email to the user with the email <{email}> address")
            else:
                user = User(email=email,
                            email_confirmation_sent_on=datetime.utcnow(),
                            username=username,
                            password=PasswordImplementer.hash_password(form.new_password.data),
                            token=token,
                            ).save()

                email_notification_to_owner_about_new_user_registration(user)
                flash("You have successfully registered.", "success")
                flash("Check your email for a confirmation link or your junk or spam box if it is not in your inbox.", "info")

            return secure_redirect_or_403(url_for("home_app.home"))
        else:
            flash("Your registration form could not be submitted because it contains errors", "danger")
    return render_template("index.html", contact_form=ContactForm(), login_form=LoginForm(), register_form=form)


@home_app.route("/home")
def landing_page() -> "render_template('index.html')":
    return render_template("index.html", contact_form=ContactForm(), login_form=LoginForm(), register_form=RegisterForm())


@home_app.route("/login", methods=["GET", "POST"])
def login() -> "render_template('index.html')":
    login_form = LoginForm()
    email = login_form.email.data

    if request.method == "POST" and login_form.validate_on_submit():
        user = User.find_by_email(email=email)

        if not user:
            flash("Incorrect Username and password", "danger")
            logger.warning(f"An unregistered user with the email <{email}> attempted to login")

        elif user and user.account and not user.account[0].live:

            flash("Your account is no longer active.", "danger")
            flash("Contact the administrator using the contact us form below", "info")

        elif user and not user.email_confirmed:
            flash("You need to confirm your email before you can use the website", "danger")

        elif user and PasswordImplementer.is_password_valid(user.password, login_form.password.data):

            session["username"] = user.username.lower()
            session["admin"] = user.account[0].admin
            session["email"] = user.email.lower()

            return secure_redirect_or_403(url_for("home_app.dashboard"))

        else:
            flash("Incorrect Username and password", "danger")
            logger.warning(f"The user <{user.username.title()}> failed to login with the correct username and password")

    return render_template("index.html", contact_form=ContactForm(), login_form=login_form, register_form=RegisterForm())


@home_app.route("/logout")
@login_required
def logout() -> "secure_redirect_or_403(url_for('home_app.home'))":

    user = User.find_by_username(session["username"])
    user.last_login = datetime.utcnow()
    user.save()
    session.clear()

    flash("You have successfully logged out", "success")
    return render_template("index.html", contact_form=ContactForm(), login_form=LoginForm(), register_form=RegisterForm())


