from flask import Blueprint
from flask import request
from flask import jsonify

from app.models import Project
from app.utils import parse_tags

bp = Blueprint(
    name="projects",
    import_name="projects",
    url_prefix="/projects"
)


@bp.get("")
def get_project_list():
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
    ).paginate(page, per_page=20, error_out=False)

    return jsonify({
        "page": {
            "max": pjs.pages,
            "this": page
        },
        "projects": [
            {
                "uuid": this.uuid,
                "title": this.title,
                "tags": parse_tags(this.tag),
                "date": this.date.strftime("%Y년 %m월 %d일"),
            } for this in pjs.items
        ]
    })
