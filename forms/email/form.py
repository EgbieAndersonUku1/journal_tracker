from wtforms.fields.html5 import EmailField
from wtforms import validators

from forms.base_form import BaseEmailForm



class ChangeEmailForm(BaseEmailForm):

    new_email = EmailField("New email", validators=[validators.DataRequired()])