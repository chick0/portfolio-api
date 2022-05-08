from re import compile
from hashlib import sha512
from random import choices
from datetime import datetime
from datetime import timedelta

from flask import Blueprint
from flask import request
from flask import jsonify

from app import db
from app.models import User
from app.models import Code
from app.mail import send_mail
from app.utils import get_ip
from app.utils import error
from app.token import get_payload
from app.token import encode_payload

bp = Blueprint(
    name="auth",
    import_name="auth",
    url_prefix="/auth"
)


@bp.post("")
def login():
    json = request.get_json(silent=True)
    try:
        email = json['email']
        password = sha512(json['password'].encode()).hexdigest()
    except (KeyError, TypeError):
        return error(
            code=400,
            message="이메일과 비밀번호를 입력해주세요."
        )

    user = User.query.filter_by(
        email=email,
        password=password
    ).first()
    if user is None:
        return error(
            code=404,
            message="이메일 또는 비밀번호가 올바르지 않습니다."
        )

    if Code.query.with_entities(Code.id).filter_by(
        owner_id=user.id,
        used=False,
    ).filter(
        Code.creation_date >= datetime.now() - timedelta(minutes=3)
    ).first() is not None:
        return error(
            code=400,
            message="다른 세션에서 로그인을 시도하고 있습니다."
        )

    code = Code()
    code.owner_id = user.id
    code.code = "".join(choices(['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'], k=6))
    code.ip = get_ip()
    code.used = False

    db.session.add(code)
    db.session.commit()

    send_mail(
        email=user.email,
        code=code.code,
        ip=code.ip,
    )

    return jsonify({
        "status": True,
        "message": "이메일로 인증 코드가 전송되었습니다. 이메일을 확인해주세요."
    })


@bp.post("/verify")
def verify():
    json = request.get_json(silent=True)
    try:
        code = json['code']
        email = json['email']
    except (KeyError, TypeError):
        return error(
            code=400,
            message="이메일과 인증 코드를 입려해주세요."
        )

    re = compile(r"\d")
    code = "".join(re.findall(code))
    if len(code) != 6:
        return error(
            code=400,
            message="올바른 인증 코드가 아닙니다."
        )

    code = Code.query.filter_by(
        code=code,
        used=False
    ).first()

    if code is None:
        return error(
            code=400,
            message="올바른 인증 코드가 아닙니다."
        )

    if code.is_expired():
        return error(
            code=400,
            message="만료된 인증 코드 입니다."
        )

    if User.query.filter_by(
        id=code.owner_id,
        email=email
    ).with_entities(User.id).first() is None:
        return error(
            code=400,
            message="올바른 인증 코드가 아닙니다."
        )

    code.used = True
    db.session.commit()

    return jsonify({
        "token": encode_payload(
            payload=get_payload(
                user_id=code.owner_id,
                code_id=code.id,
            )
        )
    })
