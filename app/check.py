
from flask import session

from app.config import get_config


def login() -> bool:
    user = get_config("User")
    us = session.get("session", {})

    chk1 = user.user == us.get("user", "")
    chk2 = user.password == us.get("password", "")

    return chk1 and chk2
