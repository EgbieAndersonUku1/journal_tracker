from datetime import datetime

from app import cache, db
from common.logger.logging import logger
from models.db_saver_helper import db_saver_helper
from models.users.user import User # Must be loaded so that it can be used with Job Model

records = db.Table("records",
                 db.Column("job_id", db.Integer, db.ForeignKey('job.id'), primary_key=True),
                 db.Column("user_id", db.Integer, db.ForeignKey('user.id'), primary_key=True)
                )


class Job(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    applied_date = db.Column(db.DateTime, default=datetime.utcnow())
    applied_job_from = db.Column(db.String(80), nullable=False)
    company = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(5000), nullable=False)
    employees = db.relationship("User", secondary=records, backref=db.backref('jobs', lazy='dynamic'))
    employment_type = db.Column(db.String(40), nullable=False)
    job_availability = db.Column(db.String(30), nullable=False)
    job_url = db.Column(db.String(600), nullable=False)
    journal = db.Column(db.String(5000))
    last_edited = db.Column(db.DateTime, default=datetime.utcnow())
    live = db.Column(db.Boolean, default=False)
    location = db.Column(db.String(80), nullable=False)
    salary = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(80), nullable=False)
    title = db.Column(db.String(80), nullable=False)

    @classmethod
    def delete_job_by_id(cls, job_id: int) -> "Job":
        """delete_job_by_id(job_id: int) -> None"""
        job = cls.find_job_by_id(job_id)
        job.live = False
        job.save()
        cache.delete(job_id)

    @classmethod
    def find_job_by_id(cls, job_id, live=True):

        job = cache.get(str(job_id))

        if not job:

            job = cls.query.filter_by(id=job_id, live=live).first_or_404()
            cache.set(str(job_id), job)
            logger.info(msg="Item was not found, adding it to cache")
        else:
            logger.info(msg=f"Retrieving item with job id {job.id} from cache")

        return job

    def save(self):
        return db_saver_helper(db, self)

    def __repr__(self):
        return "<Job title: {}>".format(self.title.title())
