from hashlib import sha512
from random import choices
from datetime import datetime
from datetime import timedelta

from flask import Blueprint
from flask import request
from flask import redirect
from flask import url_for
from flask import jsonify
from flask import render_template

from app import db
from app.models import User
from app.models import Code
from app.mail import send_mail
from app.utils import error
from app.token import get_payload
from app.token import encode_payload

bp = Blueprint(
    name="auth",
    import_name="auth",
    url_prefix="/auth"
)


@bp.get("")
def login():
    return render_template(
        "auth/login.html"
    )


@bp.post("")
def login_post():
    email = request.form.get("email", "")
    password = sha512(request.form.get("password", "").encode()).hexdigest()

    user = User.query.filter_by(
        email=email,
        password=password
    ).first()
    if user is None:
        return redirect(url_for("auth.login"))

    code = Code()
    code.owner_id = user.id
    code.code = "".join(choices(['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'], k=8))
    code.ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    code.used = False

    db.session.add(code)
    db.session.commit()

    send_mail(
        email=user.email,
        code=code.code,
        ip=code.ip,
    )

    return redirect(url_for("auth.ready"))


@bp.get("/ready")
def ready():
    return render_template(
        "auth/ready.html"
    )


@bp.post("/verify")
def verify():
    code = request.json.get("code", "").strip()
    if len(code) != 8:
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

    dead_line = code.creation_date + timedelta(minutes=3)
    if datetime.now() < dead_line:
        return error(
            code=400,
            message="만료된 인증 코드 입니다."
        )

    code.used = True
    db.session.commit()

    return jsonify({
        "token": encode_payload(
            payload=get_payload(
                id=code.owner_id
            )
        )
    })
