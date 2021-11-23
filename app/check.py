
from flask import session

from app.config import get_config


def login() -> bool:
    this_user_id = int(session.get("user", 0))

    try:
        user = get_config("User")
        allow_user_id = int(user.github_id)
    except ValueError:
        return False

    return this_user_id == allow_user_id
