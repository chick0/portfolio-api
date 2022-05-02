from flask import Blueprint
from flask import request
from flask import jsonify

from app.models import Project
from app.utils import error
from app.utils import parse_tags

bp = Blueprint(
    name="tag",
    import_name="tag",
    url_prefix="/tag"
)


@bp.get("")
def search_tag():
    try:
        page = int(request.args.get("page", "1"))

        if page <= 0:
            page = 1
    except ValueError:
        page = 1

    target = request.args.get("tag", "")

    if len(target) == 0:
        return error(
            code=400,
            message="검색할 태그를 전달받지 못했습니다."
        )

    pjs = Project.query.filter(
        Project.tag.like(f"%{target}%")
    ).with_entities(
        Project.uuid,
        Project.title,
        Project.tag,
        Project.date,
    ).order_by(
        Project.date.desc()
    ).paginate(page, per_page=8, error_out=False)

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
