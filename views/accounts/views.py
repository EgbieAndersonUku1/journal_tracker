from flask import Blueprint, flash, render_template, redirect, request, session,  url_for
from itsdangerous import SignatureExpired

from common.emails.send_emails.send_email import email_user_about_password_change, email_user_forgotten_password_link, \
    email_user_to_re_verifying_email, resend_user_expired_token_link

from common.date import format_date, get_date_now
from common.decorators import login_required
from common.errors import FailedToSendEmail
from common.generate_code import gen_confirmation_string_token_from_email
from common.logger.logging import logger
from common.logger.log_user_activity import log_account_activity
from forms.add_phone.form import AddPhoneNumberForm
from forms.email.form import ChangeEmailForm
from forms.login.form import LoginForm
from forms.password.form import ChangePasswordForm, ForgottenPasswordForm, NewPasswordForm
from models.users.user import Account, User
from utils.security.passwordImplementer import PasswordImplementer
from utils.security.secure_redirect import secure_redirect_or_403
from utils.security.token_validator import is_user_confirmation_token_valid

account_app = Blueprint("account_app", __name__)


@account_app.route("/setup/<username>")
def account_setup(username) -> "redirect(url_for('home_app.landing_page'))":

    user = User.find_by_username(username=username.lower())

    if user and not user.account:

        Account.setup_user_account(user.username)
        logger.info(msg=f"The user <{user.username.title()}> has setup their account")
        log_account_activity(username=user.username, log=f"Your account was set up on {format_date(get_date_now())}")

    elif user and user.account[0].live:
        logger.debug(msg=user.username)
        log_account_activity(username=user.username,
                             log=f"You confirmed your email address on {format_date(get_date_now())}")

    return redirect(url_for("home_app.landing_page"))


@account_app.route("/phone/add", methods=["GET", "POST"])
@login_required
def add_phone_number() -> "render_template":

    form = AddPhoneNumberForm()

    if request.method == "POST" and form.validate_on_submit():
        user = User.find_by_username(session["username"])
        user.phone_number = form.phone_number.data
        user.save()

        log = f"You added your phone number to your account on {format_date(get_date_now())}"
        log_account_activity(log=log, username=user.username)

        flash("You have successfully added your phone number", "success")
        return secure_redirect_or_403(url_for("account_app.view_account"))

    return render_template("add_details/add_phone.html", form=form, login_form=LoginForm())


@account_app.route("/email/change", methods=["GET", "POST"])
@login_required
def change_email() -> "render_template":
    form = ChangeEmailForm()

    if request.method == "POST" and form.validate_on_submit():

        user = User.find_by_email(form.email.data.strip().lower())

        if not user:
            flash("The email address used is not the same one you used to register", "danger")

        elif User.find_by_email(form.new_email.data.strip().lower()):
            flash("The new email you entered already exists", "primary")

        else:

            email = form.new_email.data.lower().strip().lower()
            token = gen_confirmation_string_token_from_email(email)

            try:
                email_user_to_re_verifying_email(email=email, username=user.username, token=token)
            except FailedToSendEmail:
                logger.critical(f"Failed to send a confirmation email to the user with the email <{email}> address")
            else:
                user.email, user.email_confirmed, user.token = email, False, token
                user.email_confirmation_sent_on = get_date_now()
                user.save()

                log = f"You successful changed your email address on {format_date(get_date_now())}"
                log_account_activity(log=log, username=user.username)

                return secure_redirect_or_403(url_for('account_app.re_verify_changed_email'))

    return render_template("add_details/change_email.html", form=ChangeEmailForm(), login_form=LoginForm())


@account_app.route("/password/change", methods=["GET", "POST"])
@login_required
def change_old_password() -> "render_template":
    form = ChangePasswordForm()

    if request.method == "POST" and form.validate_on_submit():
        user = User.find_by_username(session["username"])

        if PasswordImplementer.is_password_valid(user.password, form.password.data):
            user.password = PasswordImplementer.hash_password(form.new_password.data)
            user.save()

            email_user_about_password_change(username=user.username, email=user.email)

            log = f"You successful changed your password on {format_date(get_date_now())}"
            logger.info(f"The user <{session['username'].title()}> has changed their password")
            log_account_activity(log=log, username=user.username)

            flash("You have successfully changed your password.", "success")
            flash("The change will be implemented once you logout", "success")

        else:
            flash("Your current password does not match what we have in our records", "danger")

    return render_template("password/change_password.html", form=form, login_form=LoginForm())


@account_app.route("/account/deactivate")
@login_required
def de_activate_account() -> 'secure_redirect_or_403(url_for("account_app.successful_de_activated_account"))':

    Account.de_activate_user_account(username=session.get("username"))

    logger.info(f"The user <{session['username'].title()}> has de-activated their account")
    log_account_activity(username=session["username"], log=f"You de-activated your account on {format_date(get_date_now())}")
    session.clear()

    return secure_redirect_or_403(url_for("account_app.successful_de_activated_account"))


@account_app.route("/<username>/password/forgotten/<token>", methods=["GET", "POST"])
def reset_forgotten_password(username: str, token: str) -> "render_template":

    form = NewPasswordForm()

    user = User.find_by_username(username)

    if user and user.token != token:
        flash("The token is no longer valid", "info")
        return secure_redirect_or_403(url_for('home_app.landing_page'))

    try:
        is_user_confirmation_token_valid(user)
    except SignatureExpired:

        flash("Your token has expired a new token has been re-sent to your email", "danger")
        resend_user_expired_token_link(user)
        return secure_redirect_or_403(url_for('home_app.landing_page'))

    if request.method == "POST" and form.validate_on_submit():

        user.password = PasswordImplementer.hash_password(form.new_password.data)
        user.token = None
        user.save()

        email_user_about_password_change(username=user.username, email=user.email)

        log = f"On {format_date(get_date_now())} you successfully performed a reset on your forgotten password"
        log_account_activity(log=log, username=user.username)

        return secure_redirect_or_403(url_for("account_app.successfully_changed_password"))

    return render_template("password/new_password.html", token=token, form=form, login_form=LoginForm(), username=username)


@account_app.route("/password/reset", methods=["GET", "POST"])
def reset_password() -> "render_template":
    form = ForgottenPasswordForm()

    if request.method == "POST" and form.validate_on_submit():

        user = User.find_by_email(form.email.data)
        if user:
            token = gen_confirmation_string_token_from_email(user.email)
            email_user_forgotten_password_link(email=user.email, username=user.username, token=token)
            user.token = token
            user.save()

            logger.info(f"The user <{user.username.title()}> has requested a password reset link")
            log = f"You requested a forgotten password link on {format_date(get_date_now())}"
            log_account_activity(log=log, username=user.username)

        flash("If you email address is found we will send you a reset link", "info")

    return render_template('password/forgotten_password.html', form=form, login_form=LoginForm())


@account_app.route("/successfully_changed/email", methods=["GET", "POST"])
def re_verify_changed_email():
    session.clear()
    return render_template("success/changed_email.html", login_form=LoginForm())


@account_app.route("/successfully_changed/password", methods=["GET", "POST"])
def successfully_changed_password():
    session.clear()
    return render_template("success/password.html", login_form=LoginForm())


@account_app.route("/account/deactivated")
def successful_de_activated_account():
    return render_template("account/account_deactivated.html", login_form=LoginForm())


@account_app.route("/account")
@login_required
def view_account() -> "render_template":

    user = User.find_by_username(session["username"])
    return render_template("account/account.html", login_form=LoginForm(), user=user)


@account_app.route("/account/history")
@login_required
def view_history() -> "render_template":

    ROWS_PER_PAGE = 15
    page = request.args.get('page', 1, type=int)

    histories = Account.get_account_activity_history_by_username(session["username"]).paginate(page=page, per_page=ROWS_PER_PAGE)
    return render_template("history/history.html", login_form=LoginForm(), histories=histories)



