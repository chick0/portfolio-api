from flask import Blueprint
from flask import jsonify

from app.github import build_url
from app import auth
from app.token import check

bp = Blueprint(
    name="auth",
    import_name="auth",
    url_prefix="/auth"
)

for service in auth.__all__:
    bp.register_blueprint(
        blueprint=getattr(getattr(auth, service), "bp")
    )


@bp.get("/get-url")
def get_url():
    return jsonify({
        "github": build_url(),
    })


@bp.get("/test")
def test():
    result = check()
    if result is None:
        return jsonify({
            "message": "해당 토큰은 유효한 토큰 입니다."
        }), 200
    else:
        return jsonify({
            "message": result.message
        }), result.status
