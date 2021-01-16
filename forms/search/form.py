from flask import session
from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from forms.choices import JOBS_SITES
from models.users.user import User
from models.jobs.job import Job
from forms import choices


def search_form_query() -> "Job":
    return User.get_user_jobs(session["username"])


class SearchForm(FlaskForm):
    job_title = QuerySelectField("Job title", query_factory=search_form_query, allow_blank=True, get_label="title")
    company = QuerySelectField("Company", query_factory=search_form_query, allow_blank=True, get_label="company")
    applied_job_from = SelectField("Where did your find the job?", choices=JOBS_SITES)
    employment_type = SelectField("Employment type", choices=choices.EMPLOYMENT_TYPE)
    countries = SelectField("Country", choices=choices.COUNTRIES)

    min_salary = SelectField("Sal (Min)", choices=choices.MIN)
    max_salary = SelectField("Sal (Max)", choices=choices.MAX)
    job_status = SelectField("Status", choices=choices.JOB_STATUS)


