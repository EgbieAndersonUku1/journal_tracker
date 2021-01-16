from wtforms import StringField, validators, TextAreaField

from forms.base_form import BaseEmailForm


class ContactForm(BaseEmailForm):

    first_name = StringField("First name", validators=[validators.Length(min=3, max=40)])
    surname = StringField("Surname", validators=[validators.Length(min=3, max=40)])
    message = TextAreaField("Message", render_kw={"class": "form-control", "rows": 10},
                                       validators=[validators.DataRequired(),
                                       validators.Length(min=1000)])

