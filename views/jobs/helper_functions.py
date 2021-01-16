from sqlalchemy import and_

from forms.jobs.form import JobForm
from models.jobs.job import Job


def filter_jobs_query_based_on_search_form_parameter(job: "Job.query", form: "JobForm") -> "Job.query":
    """filter_jobs(job sqlalchemy query) -> Job query object

       Take a job query object and filters the query based on
       the Job model parameters
    """
    return job.filter(Job.location == form.countries.data,
                      Job.status == form.job_status.data,
                      Job.employment_type == form.employment_type.data,
                      Job.applied_job_from == form.applied_job_from.data,
                      ).filter(and_(Job.salary >= form.min_salary.data, Job.salary <= form.max_salary.data))



