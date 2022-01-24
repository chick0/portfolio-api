from flask import Blueprint
from flask import jsonify

from app.github import build_url
from app import auth

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
