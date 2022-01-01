from uuid import uuid4

from flask import Blueprint
from flask import abort
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template

from app import db
from app.models import Project
from app.check import login

bp = Blueprint(
    name="editor",
    import_name="editor",
    url_prefix="/editor"
)


@bp.get("")
def ready():
    if not login():
        return redirect(url_for("session.login"))

    try:
        page = int(request.args.get("page", "1"))

        if page <= 0:
            page = 1
    except ValueError:
        page = 1

    projects = Project.query.with_entities(
        Project.uuid,
        Project.title,
    ).order_by(
        Project.date.desc()
    ).paginate(page)

    return render_template(
        "editor/ready.html",
        pjs=projects.items,
        pg_prev=projects.prev_num,
        pg_next=projects.next_num,
        page=page
    )


@bp.get("/<string:project_id>")
def editor(project_id: str):
    if not login():
        return redirect(url_for("session.login"))

    pj = Project.query.filter_by(
        uuid=project_id
    ).first()

    if pj is None:
        return abort(404)

    try:
        page = int(request.args.get("page", "1"))

        if page <= 0:
            page = 1
    except ValueError:
        page = None

    if page == 1:
        page = None

    return render_template(
        "editor/editor.html",
        editor=True,
        pj=pj,
        page=page
    )


@bp.post("/<string:project_id>")
def editor_post(project_id: str):
    if not login():
        return redirect(url_for("session.login"))

    pj = Project.query.filter_by(
        uuid=project_id
    ).first()

    if pj is None:
        return abort(404)

    pj.title = request.form.get("title")
    pj.date = request.form.get("date")
    pj.tag = request.form.get("tag")
    pj.web = request.form.get("web")
    pj.github = request.form.get("github")
    pj.a = request.form.get("a").replace("\r\n", "\n")
    pj.b = request.form.get("b").replace("\r\n", "\n")
    pj.c = request.form.get("c").replace("\r\n", "\n")

    db.session.commit()

    try:
        page = int(request.args.get("page", "1"))

        if page <= 0:
            page = 1
    except ValueError:
        page = None

    if page == 1:
        page = None

    return redirect(url_for("editor.ready", page=page))


@bp.get("/new")
def new():
    if not login():
        return redirect(url_for("session.login"))

    try:
        page = int(request.args.get("page", "1"))

        if page <= 0:
            page = 1
    except ValueError:
        page = None

    if page == 1:
        page = None

    return render_template(
        "editor/new.html",
        editor=True,
        page=page
    )


@bp.post("/new")
def new_post():
    if not login():
        return redirect(url_for("session.login"))

    pj = Project()
    pj.uuid = uuid4().__str__()
    pj.title = request.form.get("title")
    pj.date = request.form.get("date")
    pj.tag = request.form.get("tag")
    pj.web = request.form.get("web")
    pj.github = request.form.get("github")
    pj.a = request.form.get("a").replace("\r\n", "\n")
    pj.b = request.form.get("b").replace("\r\n", "\n")
    pj.c = request.form.get("c").replace("\r\n", "\n")

    db.session.add(pj)
    db.session.commit()

    return redirect(url_for("editor.editor", project_id=pj.uuid))
