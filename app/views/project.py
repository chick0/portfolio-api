from flask import Blueprint
from flask import jsonify

from app.models import Project
from app.utils import error
from app.utils import parse_tags

bp = Blueprint(
    name="project",
    import_name="project",
    url_prefix="/project"
)


@bp.get("/<string:project_id>")
def get_project(project_id: str):
    if len(project_id) != 36:
        return error(
            code=400,
            message="프로젝트 아이디가 올바르지 않습니다."
        )

    pj = Project.query.filter_by(
        uuid=project_id
    ).first()

    if pj is None:
        return error(
            code=404,
            message="해당 프로젝트를 찾지 못했습니다."
        )

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
