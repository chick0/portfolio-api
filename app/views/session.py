
from flask import Blueprint
from flask import session
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template

from app.config import get_config
from app.config.models import User
from app.login import get_user
from app.check import login as chk_login


bp = Blueprint(
    name="session",
    import_name="session",
    url_prefix="/session"
)


@bp.get("")
@bp.get("/")
def auto_redirect():
    if chk_login():
        return redirect(url_for("editor.ready"))

    return redirect(url_for("session.login"))


@bp.get("/login")
def login():
    if chk_login():
        return redirect(url_for("editor.ready"))

    return render_template(
        "session/login.html"
    )


@bp.post("/login")
def login_post():
    if chk_login():
        return redirect(url_for("editor.ready"))

    user = get_user(
        User(
            user=request.form.get("user"),
            password=request.form.get("pass")
        )
    )

    user_from_config = get_config("User")

    chk1 = user.user == user_from_config.user
    chk2 = user.password == user_from_config.password

    if chk1 and chk2:
        session['session'] = {
            "user": user.user,
            "password": user.password
        }

        return redirect(url_for("editor.ready"))

    return redirect(url_for("session.login"))


@bp.get("/logout")
def logout():
    for key in list(session.keys()):
        del session[key]

    return redirect(url_for("session.login"))
