from flask import Blueprint
from flask import jsonify

from app.utils import login_required

bp = Blueprint("token", __name__, url_prefix="/token")


@bp.get("/verify")
@login_required
def verify(payload: dict):
    return jsonify({
        "status": True
    })
