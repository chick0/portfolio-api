from uuid import uuid4
from datetime import datetime

from flask import Blueprint
from flask import request
from flask import jsonify
from sqlalchemy.exc import IntegrityError

from app import db
from app.models import Project
from app.token import check

bp = Blueprint(
    name="manage",
    import_name="manage",
    url_prefix="/manage"
)


@bp.post("/new")
def project_new():
    result = check()
    if result is not None:
        return jsonify({"message": result.message}), \
               result.status

    json = request.json

    pj = Project()
    pj.uuid = uuid4().__str__()

    pj.title = json.get("title", "[작성중]")
    pj.tag = json.get("tag", "")
    pj.web = json.get("web", "")
    pj.github = json.get("github", "")
    pj.a = json.get("a", "기획의도 작성중").replace("\r\n", "\n")
    pj.b = json.get("b", "특징 작성중").replace("\r\n", "\n")
    pj.c = json.get("c", "느낀점 작성중").replace("\r\n", "\n")

    date_str = json.get("date")
    if date_str is None:
        date = datetime.today()
    else:
        date = datetime.strptime(date_str, "%Y-%m-%d")

    pj.date = date

    try:
        db.session.add(pj)
        db.session.commit()
    except IntegrityError:
        return jsonify({
            "message": "프로젝트 아이디 중복 발생"
        }), 500

    return jsonify({
        "message": "프로젝트 생성완료",
        "uuid": pj.uuid
    })


@bp.post("/<string:project_id>")
def project_update(project_id: str):
    result = check()
    if result is not None:
        return jsonify({"message": result.message}), \
               result.status

    if len(project_id) != 36:
        return jsonify({
            "message": "프로젝트 아이디가 올바르지 않습니다."
        }), 400

    pj = Project.query.filter_by(
        uuid=project_id
    ).first()

    if pj is None:
        return jsonify({
            "message": "저장할 프로젝트를 찾지 못했습니다."
        }), 400

    json = request.json

    pj.title = json.get("title", pj.title)
    pj.tag = json.get("tag", pj.tag)
    pj.web = json.get("web", pj.web)
    pj.github = json.get("github", pj.github)
    pj.a = json.get("a", pj.a).replace("\r\n", "\n")
    pj.b = json.get("b", pj.b).replace("\r\n", "\n")
    pj.c = json.get("c", pj.c).replace("\r\n", "\n")

    date_str = json.get("date")
    if date_str is None:
        date = pj.date
    else:
        date = datetime.strptime(date_str, "%Y-%m-%d")

    pj.date = date

    db.session.commit()

    return jsonify({
        "message": "프로젝트 저장완료"
    })


@bp.delete("/<string:project_id>")
def project_del(project_id: str):
    result = check()
    if result is not None:
        return jsonify({"message": result.message}), \
               result.status

    pj = Project.query.with_entities(
        Project.title
    ).filter_by(
        uuid=project_id
    ).first()

    if pj is None:
        return jsonify({
            "message": "삭제할 프로젝트를 찾지 못했습니다."
        }), 400

    Project.query.filter_by(
       uuid=project_id
    ).delete()
    db.session.commit()

    return jsonify({
        "message": f"'{pj.title}' 프로젝트가 삭제되었습니다."
    })
