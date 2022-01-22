from urllib.parse import urlparse

from flask import Blueprint
from flask import request
from flask import jsonify

from app.models import Project

bp = Blueprint(
    name="api",
    import_name="api",
    url_prefix="/api"
)


@bp.get("/projects")
def projects():
    try:
        page = int(request.args.get("page", "1"))

        if page <= 0:
            page = 1
    except ValueError:
        page = 1

    pjs = Project.query.with_entities(
        Project.uuid,
        Project.title,
        Project.tag,
        Project.date,
    ).order_by(
        Project.date.desc()
    ).paginate(page, per_page=8)

    return jsonify({
        "page": {
            "max": pjs.pages,
            "this": page
        },
        "projects": [
            {
                "uuid": this.uuid,
                "title": this.title,
                "tag": this.tag,
                "tags": [tag.strip() for tag in this.tag.split(",")],
                "date": this.date.strftime("%Y년 %m월 %d일"),
            } for this in pjs.items
        ]
    })


@bp.get("/project/<string:project_id>")
def project(project_id: str):
    if len(project_id) != 36:
        return jsonify({
            "status": "fail",
            "error": {
                "code": "uuid_length_error",
                "message": "프로젝트 아이디가 올바르지 않습니다."
            }
        }), 400

    pj = Project.query.filter_by(
        uuid=project_id
    ).first()

    if pj is None:
        return jsonify({
            "status": "fail",
            "error": {
                "code": "project_not_found",
                "message": "해당 프로젝트를 조회하지 못했습니다."
            }
        }), 404

    github = pj.github
    if github is None:
        github = ""

    return jsonify({
        "title": pj.title,
        "date": pj.date.strftime("%Y년 %m월 %d일"),
        "tag": pj.tag,
        "tags": [tag.strip() for tag in pj.tag.split(",")],
        "web": pj.web,
        "github": github,
        "github_preview": urlparse(github).path.replace("/", " ").strip().replace(" ", "/"),
        "content": {
            "a": pj.a,
            "b": pj.b,
            "c": pj.c
        },
    })


@bp.get("/tag")
def search_tag():
    try:
        page = int(request.args.get("page", "1"))

        if page <= 0:
            page = 1
    except ValueError:
        page = 1

    target = request.args.get("tag", "")

    if len(target) == 0:
        return jsonify({
            "status": "fail",
            "error": {
                "code": "tag_missing",
                "message": "검색할 태그를 전달받지 못했습니다."
            }
        }), 400

    pjs = Project.query.filter_by(
        tag=f"%{target}%"
    ).with_entities(
        Project.uuid,
        Project.title,
        Project.tag,
        Project.date,
    ).order_by(
        Project.date.desc()
    ).paginate(page, per_page=8)

    return jsonify({
        "page": {
            "max": pjs.pages,
            "this": page
        },
        "projects": [
            {
                "uuid": this.uuid,
                "title": this.title,
                "tags": [tag.strip() for tag in this.tag.split(",")],
                "date": this.date.strftime("%Y년 %m월 %d일"),
            } for this in pjs.items
        ]
    })
