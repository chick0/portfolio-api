from time import time as timestamp

from flask import Blueprint
from flask import request
from flask import jsonify

from app import db
from app.models import Code
from app.utils import error
from app.utils import login_required
from app.token import get_payload
from app.token import encode_payload

bp = Blueprint("token", __name__, url_prefix="/token")


@bp.get("/verify")
@login_required
def verify(payload: dict):
    now = round(timestamp())
    return jsonify({
        "status": True,
        "renew_required": payload['time']['b'] - now <= 3600
    })


@bp.get("/renew")
@login_required
def renew(payload: dict):
    code = Code.query.filter_by(
        id=payload['code_id']
    ).first()

    if code is None or code.code == "#":
        return error(
            code=400,
            message="인증 코드 정보가 삭제된 인증 토큰 입니다."
        )

    if code.code == "-":
        return error(
            code=400,
            message="해당 인증 토큰은 연장 할 수 없습니다."
        )

    nc = Code()
    nc.owner_id = code.owner_id
    nc.code = "-"
    nc.ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    nc.used = True

    db.session.add(nc)
    db.session.commit()

    return jsonify({
        "token": encode_payload(
            payload=get_payload(
                user_id=code.owner_id,
                code_id=nc.id,
                host=payload['host'],
                client=payload['client'],
            )
        )
    })


@bp.get("/history")
@login_required
def history(payload: dict):
    codes = []
    for code in Code.query.filter_by(
        owner_id=payload['user_id']
    ).order_by(
        Code.id.desc()
    ).limit(60).all():
        codes.append(code.to_json())

    return jsonify({
        "history": codes
    })


@bp.delete("/code/<int:code_id>")
@login_required
def revoke_code(payload: dict, code_id: int):
    code = Code.query.filter_by(
        id=code_id,
    ).first()

    code.code = "#"

    db.session.commit()

    return jsonify({
        "status": True
    })
