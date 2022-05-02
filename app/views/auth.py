from flask import Blueprint
from flask import render_template

bp = Blueprint(
    name="auth",
    import_name="auth",
    url_prefix="/auth"
)


@bp.get("")
def login():
    return render_template(
        ""
    )
