from flask import Blueprint
from flask import jsonify

from app.models import Project
from app.tools import parse_tags

bp = Blueprint(
    name="project",
    import_name="project",
    url_prefix="/project"
)


@bp.get("/<string:project_id>")
def get_project(project_id: str):
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
        "dt": pj.date.strftime("%Y-%m-%d"),
        "date": pj.date.strftime("%Y년 %m월 %d일"),
        "tags": parse_tags(pj.tag),
        "web": pj.web,
        "github": github,
        "content": {
            "a": pj.a,
            "b": pj.b,
            "c": pj.c
        },
    })
