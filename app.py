from flask import Flask, render_template
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
from flask_wtf.csrf import CSRFProtect


from common.logger.logging import logger
from forms.login.form import LoginForm
from settings import CONFIG

app = Flask(__name__)


cache = Cache()
ckeditor = CKEditor()
csrf = CSRFProtect(app)
db = SQLAlchemy()


def bad_request(error):
    logger.critical(msg=error)
    return render_template("errors/bad_request.html", login_form=LoginForm()), 400


def internal_error(error):
    logger.critical(msg=error)
    db.session.rollback()
    return render_template("errors/internal_error.html", login_form=LoginForm()), 500


def not_authorized(error):

    from flask import session
    logger.critical(msg=error)
    logger.critical(msg=f"An authorised attempt was made by the user with email {session.get('email') } and the username {session.get('username')}")
    return render_template("errors/unauthorized_access.html", login_form=LoginForm()), 403


def page_not_found(error):
    logger.critical(msg=error)
    return render_template("errors/page_not_found.html", login_form=LoginForm()), 404



def create_app(**config_overrides):

    app.config.from_pyfile("settings.py")

    app.config.update(config_overrides)



    db.init_app(app)
    ckeditor.init_app(app)
    cache.init_app(app, config=CONFIG)

    from views.accounts.views import account_app
    from views.admin.views import admin_app
    from views.home.views import home_app
    from views.jobs.views import job_app

    app.register_blueprint(account_app)
    app.register_blueprint(admin_app)
    app.register_blueprint(home_app)
    app.register_blueprint(job_app)

    app.register_error_handler(400, bad_request)
    app.register_error_handler(500, internal_error)
    app.register_error_handler(403, not_authorized)
    app.register_error_handler(404, page_not_found)

    return app


