from flask import Blueprint, flash, render_template

from common.decorators import admin_required
from forms.login.form import LoginForm
from models.users.user import Account

admin_app = Blueprint("admin_app", __name__)


@admin_app.route("/admin")
@admin_required
def admin():
    return render_template("admin/under_construction.html", login_form=LoginForm())


@admin_app.route("/admin")
@admin_required
def activate_account() -> "render_template":

    # Account.activate_user_account(username.lower())
    # flash(f"You re-activated the account for user {username.title()}")
    return render_template("admin/under_construction.html", login_form=LoginForm())



