from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, validators

from forms.choices import COUNTRIES_PHONE_NUMBER


class AddPhoneNumberForm(FlaskForm):
    countries = SelectField("Countries", choices=COUNTRIES_PHONE_NUMBER)
    phone_number = IntegerField("Phone number",
                                validators=[validators.DataRequired(message="The number must be an integer")])
