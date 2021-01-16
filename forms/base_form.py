from flask_wtf import FlaskForm
from wtforms import validators, PasswordField
from wtforms.fields.html5 import EmailField


class BaseEmailForm(FlaskForm):
    email = EmailField("Email", validators=[validators.DataRequired()])



class BaseBasicPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[validators.DataRequired(),
                                                     validators.Length(min=8, max=90),
                                                     ]
                             )


class BasePasswordForm(FlaskForm):
    new_password = PasswordField("New Password", validators=[validators.DataRequired(),
                                                         validators.Length(min=8, max=90),
                                                         validators.EqualTo("confirm"),
                                                         ]
                                 )
    confirm = PasswordField("Confirm password")
