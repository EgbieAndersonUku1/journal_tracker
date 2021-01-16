from wtforms import PasswordField, validators

from forms.base_form import BaseBasicPasswordForm, BasePasswordForm, BaseEmailForm



class ChangePasswordForm(BaseBasicPasswordForm, BasePasswordForm):
    password = PasswordField("Current Password", validators=[validators.DataRequired(),
                                                     validators.Length(min=8, max=90),
                                                     ]
                             )


class ForgottenPasswordForm(BaseEmailForm):
    pass



class NewPasswordForm(BasePasswordForm):
    pass