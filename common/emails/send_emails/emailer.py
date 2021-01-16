import smtplib

from dataclasses import dataclass, field
from os import environ

from common.errors import FailedToSendEmail
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


@dataclass
class EmailSender:

    sender_email: str = field(init=False, repr=False, default=environ.get("EMAIL_ADDRESS"))
    sender_password: str = field(init=False, repr=False, default=environ.get("EMAIL_PASSWORD"))
    receiver_email: str
    subject: str
    text: str
    html: str
    _session: "smtplib.SMTP" = field(repr=False, default=None)
    _msg: "MIMEMultipart" = field(repr=False, default=None)

    def send(self) -> bool:
        self._start_secure_connection()
        self._setup_mime_msg()

        try:
            self._session.sendmail(EmailSender.sender_email, self.receiver_email, self._msg.as_string())
            self._session.quit()
        except:
            raise FailedToSendEmail("There was an error sending your email")
        return True

    def _start_secure_connection(self) -> None:
        self._session = smtplib.SMTP("smtp.gmail.com", "587")

        self._session.starttls()

        self._session.login(EmailSender.sender_email, EmailSender.sender_password)

    def _setup_mime_msg(self) -> None:
        """Setup the message to be send to that will be send to the user"""

        msg = MIMEMultipart("alternative")
        msg["from"] = EmailSender.sender_email
        msg["To"] = self.receiver_email
        msg["Subject"] = self.subject

        text_part = MIMEText(self.text, "plain")
        html_part = MIMEText(self.html, "html")

        msg.attach(text_part)
        msg.attach(html_part)
        self._msg = msg


