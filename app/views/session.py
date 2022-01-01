from flask import Blueprint
from flask import session
from flask import request
from flask import redirect
from flask import url_for

from app.check import login as chk_login
from app.github import build_url
from app.github import generate_access_token
from app.github import get_user

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

    return redirect(build_url())


@bp.get("/logout")
def logout():
    is_login = chk_login()

    for key in list(session.keys()):
        del session[key]

    return {
        True:  "로그아웃 완료!",
        False: "로그인 상태가 아닙니다.",
    }.get(is_login)


@bp.get("/callback")
def callback():
    code = request.args.get("code", "#")

    access_token = generate_access_token(code=code)
    if access_token.token == "":
        return redirect(url_for("session.login"))

    user = get_user(access_token)

    session['user'] = user.id

    if not chk_login():
        return redirect(url_for("session.logout"))

    return redirect(url_for("editor.ready"))
