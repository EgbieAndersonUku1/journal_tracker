from os import environ

from common.emails.email_templates.change_password_confirmation.confirmation import \
    PASSWORD_CHANGE_CONFIRMATION_HTML, PASSWORD_CHANGE_CONFIRMATION_TEXT

from common.emails.send_emails.emailer import EmailSender
from common.emails.email_templates.contact_message.contact_message import\
    CONTACT_MESSAGE_HTML, CONTACT_MESSAGE_TEXT, RESPONSE_CONTACT_MESSAGE_TEXT, RESPONSE_CONTACT_MESSAGE_HTML

from common.emails.email_templates.forgotten_password.forgotten_password import FORGOTTEN_PASSWORD_HTML, FORGOTTEN_PASSWORD_TEXT
from common.emails.email_templates.registration_confirmation.confirmation import EMAIL_CONFIRMATION_TEXT, EMAIL_CONFIRMATION_HTML
from common.emails.email_templates.resend_expired_confirmation_template.resend_confirmation_link \
    import RE_SEND_CONFIRMATION_LINK_HTML, RE_SEND_CONFIRMATION_LINK_TEXT

from common.emails.email_templates.email_confirmation.verify_email import RE_VERIFY_EMAIL_HTML, RE_VERIFY_EMAIL_TEXT
from common.generate_code import gen_confirmation_string_token_from_email
from common.emails.email_templates.new_user.new_user import NEW_USER_HTML, NEW_USER_TEXT
from settings import HOSTNAME


def email_notification_to_owner_about_new_user_registration(user):

    subject = "re: A new user has registered to the website"

    username = user.username.title()
    html = NEW_USER_HTML.format(username, user.email)
    text = NEW_USER_TEXT.format(username, user.email)
    return EmailSender(receiver_email=environ.get("EMAIL_ADDRESS"), subject=subject, text=text, html=html).send()


def email_user_about_password_change(username: str, email: str) -> bool:

    subject = "Re: Password change"
    return _email_sender_helper(HOSTNAME,
                                PASSWORD_CHANGE_CONFIRMATION_HTML,
                                subject,
                                PASSWORD_CHANGE_CONFIRMATION_TEXT,
                                email=email,
                                username=username,
                                token=None,
                                )


def email_user_confirmation_email_link(username: str, email: str, token: str) -> bool:

    subject = "Re: In order to use the application you need to confirm your email"

    return _email_sender_helper(HOSTNAME,
                                EMAIL_CONFIRMATION_HTML,
                                subject,
                                EMAIL_CONFIRMATION_TEXT,
                                email=email,
                                username=username,
                                token=token
                                )


def email_user_forgotten_password_link(username: str, email: str, token: str) -> bool:

    subject = "Re: Forgotten password link reset"

    return _email_sender_helper(HOSTNAME,
                                FORGOTTEN_PASSWORD_HTML,
                                subject,
                                FORGOTTEN_PASSWORD_TEXT,
                                email=email,
                                username=username,
                                token=token,
                                )


def email_user_to_re_verifying_email(username: str, email: str, token: str) -> bool:

    subject = "Re: In order to use the application you need to confirm your email"

    return _email_sender_helper(HOSTNAME,
                                RE_VERIFY_EMAIL_HTML,
                                subject,
                                RE_VERIFY_EMAIL_TEXT,
                                email=email,
                                username=username.title(),
                                token=token
                                )


def resend_user_expired_token_link(user):
    token = gen_confirmation_string_token_from_email(user.email)
    user.token = token
    user.save()
    resend_expire_email_confirmation_email_link(username=user.username, email=user.email, token=token)



def resend_expire_email_confirmation_email_link(username: str, email: str, token: str):

    subject = "Re: Your confirmation link has expired"

    return _email_sender_helper(HOSTNAME,
                                RE_SEND_CONFIRMATION_LINK_HTML,
                                subject,
                                RE_SEND_CONFIRMATION_LINK_TEXT,
                                email=email,
                                username=username,
                                token=token
                                )


def send_user_contact_message(first_name, surname, email, message) -> bool:

    contact_html = CONTACT_MESSAGE_HTML.format(first_name.title(), surname.title(), message)
    contact_text = CONTACT_MESSAGE_TEXT.format(first_name.title(), surname.title(), message)
    subject = "Re: A message was send to you"

    response_html = RESPONSE_CONTACT_MESSAGE_HTML.format(first_name.title(), surname.title(), message)
    response_text = RESPONSE_CONTACT_MESSAGE_TEXT.format(first_name.title(), surname.title(), message)
    response_subj = "Re: Thank you for message"

    EmailSender(receiver_email=environ.get("EMAIL_ADDRESS"), subject=subject, text=contact_text,
                html=contact_html).send()

    return EmailSender(receiver_email=email, subject=response_subj, text=response_text, html=response_html).send()


def _email_sender_helper(host_name, html_template, subject, text_template, **kwargs):
    username = kwargs["username"].title()
    html = html_template.format(username, host_name, username, kwargs["token"])
    text = text_template.format(username, host_name, username, kwargs["token"])

    return EmailSender(receiver_email=kwargs["email"],
                       subject=subject,
                       text=text,
                       html=html
                       ).send()



