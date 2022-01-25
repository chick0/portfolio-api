from uuid import uuid4
from flask import Blueprint
from flask import request
from flask import jsonify
from jwt import decode
from jwt.exceptions import InvalidSignatureError

from app import db
from app.models import Project
from app.secret_key import SECRET_KEY
from app.token import check

bp = Blueprint(
    name="manage",
    import_name="manage",
    url_prefix="/manage"
)

@bp.delete("/<string:project_id>")
def project_del(project_id: str):
    try:
        authorization = request.headers.get("authorization")
        tp, token = authorization.split(" ")

        if tp != "Bearer":
            raise ValueError
    except ValueError:
        return jsonify({
            "message": "인증 토큰이 없습니다."
        }), 400

    try:
        token = decode(
            jwt=token,
            key=SECRET_KEY.hex(),
            algorithms=["HS256"]
        )
    except InvalidSignatureError:
        return jsonify({
            "message": "인증키가 올바르지 않습니다"
        }), 400

    result = check(token=token)
    print(result)

    if not isinstance(result, bool):
        return jsonify({"message": result.message}),\
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
