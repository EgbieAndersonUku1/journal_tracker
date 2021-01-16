from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import FloatField, SelectField, StringField,  validators
from wtforms.fields.html5 import URLField

from forms.choices import COUNTRIES, EMPLOYMENT_TYPE, JOBS_AVAILABILITY, JOBS_SITES, JOB_STATUS


class JobForm(FlaskForm):

    applied_job_from = SelectField("Where did your find the job?", choices=JOBS_SITES)
    company = StringField("Company", validators=[validators.DataRequired(), validators.Length(min=3, max=80)])
    description = CKEditorField("Job description", validators=[validators.DataRequired(), validators.Length(min=255)])
    employment_type = SelectField("Employment contract", choices=EMPLOYMENT_TYPE)
    job_availability = SelectField("job availability on the site", choices=JOBS_AVAILABILITY)
    job_url = URLField("Job URL", validators=[validators.DataRequired(message="Invalid URL format"),
                                              validators.Length(max=600)])
    journal = CKEditorField("Job journal e.g. preparing for job by watching videos, etc",
                            validators=[validators.DataRequired(message="The minimum characters is 255 characters"),
                                        validators.Length(min=255)])
    location = SelectField("Location", choices=COUNTRIES)
    salary = FloatField("Pay", validators=[validators.DataRequired(message="This must be an integer or a float")])
    status = SelectField("Status", choices=JOB_STATUS)
    title = StringField("Title", validators=[validators.DataRequired(), validators.Length(min=3, max=80)])




