from time import time

from flask import Blueprint
from flask import request
from flask import jsonify
from jwt import encode

from app.secret_key import SECRET_KEY
from app.config import get_config
from app.github import generate_access_token
from app.github import get_user

bp = Blueprint(
    name="github",
    import_name="github",
    url_prefix="/github"
)


@bp.get("/callback")
def callback():
    def check_id(this: int) -> bool:
        try:
            allow_id = int(get_config("User").github_id)
        except ValueError:
            return False

        return this == allow_id

    code = request.args.get("code", "#")

    access_token = generate_access_token(code=code)
    if access_token.token == "":
        return jsonify({
            "result": False,
            "token": ""
        }), 400

    user = get_user(access_token)

    if check_id(user.id):
        a = int(time())

        return jsonify({
            "result": True,
            "token": encode(
                payload={
                    "id": user.id,
                    "time": {
                        "a": a,
                        "b": a + (6 * 3600)
                    },
                    "host": request.host,
                    "client": request.referrer,
                    "type": "github"
                },
                key=SECRET_KEY.hex(),
                algorithm="HS256"
            )
        })

    return jsonify({
        "result": False,
        "token": ""
    }), 400
