from flask import abort, Blueprint, flash, render_template, request, session, url_for
from sqlalchemy import and_

from app import cache
from common.date import format_date, get_date_now
from common.decorators import login_required
from common.logger.log_user_activity import log_account_activity
from forms.jobs.form import JobForm
from forms.login.form import LoginForm
from forms.search.form import SearchForm
from models.jobs.job import Job
from models.users.user import User
from views.jobs.helper_functions import filter_jobs_query_based_on_search_form_parameter
from utils.security.secure_redirect import secure_redirect_or_403

job_app = Blueprint("job_app", __name__)

_ROWS_PER_PAGE = 8


@job_app.route("/jobs/add/job", methods=["GET", "POST"])
@login_required
def add_job() -> "render_template('job/add_job.html')":

    form = JobForm()
    edit = False

    if request.method == "POST" and form.validate_on_submit():
        user = User.find_by_username(session["username"])

        if user:
            job = Job(applied_job_from=form.applied_job_from.data,
                      company=form.company.data,
                      description=form.description.data,
                      employment_type=form.employment_type.data,
                      job_availability=form.job_availability.data,
                      job_url=form.job_url.data,
                      journal=form.journal.data,
                      live=True,
                      location=form.location.data,
                      salary=form.salary.data,
                      status=form.status.data,
                      title=form.title.data,
                      )

            job.save()
            user.jobs.append(job)
            user.save()


            log = f"You added the job with ID {job.id} on the {format_date(job.applied_date)} to the database"
            log_account_activity(username=session["username"], log=log)

            flash("Successfully added job to the database", "success")

            return secure_redirect_or_403(url_for('job_app.add_job'))

    return render_template("job/add_job.html", edit=edit, form=form, login_form=LoginForm())


@job_app.route("/job/delete/<job_id>", methods=["GET", "POST"])
@login_required
def delete_job(job_id: int) -> "render_template(url_for('job_app.jobs'))":

    Job.delete_job_by_id(job_id)

    log = f"You deleted a job with id {job_id} from the database on the {format_date(get_date_now())}"
    log_account_activity(username=session["username"], log=log)

    flash("You have successfully deleted the job from the database", "success")
    return secure_redirect_or_403(url_for("job_app.jobs"))


@job_app.route("/job/edit/<int:job_id>", methods=["GET", "POST"])
@login_required
def edit_job(job_id: int) -> "render_template('job/add_job.html')":

    edit = True

    job = Job.find_job_by_id(job_id)
    form = JobForm(obj=job)

    if request.method == "POST" and form.validate_on_submit():
        job_id = str(job_id)
        form.populate_obj(job)
        job.last_edited = get_date_now()


        cache.delete(job_id)
        cache.set(key=job_id, value=job)
        job.save()

        log = f"You successful edited a job with ID {job_id} on the {format_date(job.applied_date)}"
        log_account_activity(session["username"], log)

        flash("You have successfully edited your job", "success")
        return secure_redirect_or_403(url_for('job_app.get_job_with_id', job_id=job_id))

    return render_template("job/add_job.html", form=form, login_form=LoginForm(), edit=edit, job_id=job_id)


@job_app.route("/jobs/<job_id>")
@login_required
def get_job_with_id(job_id: str) -> "render_template('job/job.html')":
    return render_template("job/job.html", job=Job.find_job_by_id(job_id), login_form=LoginForm())


@job_app.route("/jobs")
@login_required
def jobs() -> "render_template('job/jobs.html')":

    page = request.args.get('page', 1, type=int)
    jobs = User.get_user_jobs(session["username"]).order_by(Job.id.desc()).paginate(page=page, per_page=_ROWS_PER_PAGE)
    return render_template("job/jobs.html", jobs=jobs, login_form=LoginForm())


@job_app.route("/jobs/search")
@login_required
def search() -> "render_template('search/search.html')":
    return render_template("search/search.html", login_form=LoginForm(), form=SearchForm())


@job_app.route("/jobs/search/queries", methods=["GET", "POST"])
@login_required
def queried_job_search() -> "render_template('search/job_searches.html')":

    form = SearchForm()
    page = request.args.get('page', 1, type=int)

    if form.validate_on_submit():

        jobs = User.get_user_jobs(session["username"])

        if form.job_title.data and not form.company.data:
            jobs = jobs.filter(Job.title == form.job_title.data.title)

        elif not form.job_title.data and form.company.data:
            jobs = jobs.filter(Job.company == form.company.data.company)

        elif form.job_title.data and form.company.data:
            jobs = jobs.filter(and_(Job.title == form.job_title.data.title, Job.company == form.company.data.company))

        jobs = filter_jobs_query_based_on_search_form_parameter(jobs, form).paginate(page=page, per_page=_ROWS_PER_PAGE)

        return render_template("search/job_searches.html", login_form=LoginForm(), form=form, jobs=jobs)
    return abort(404)