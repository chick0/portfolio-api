from time import time as timestamp
from datetime import timedelta

from flask import request
from jwt import encode

from app.secret_key import SECRET_KEY

algorithms = ['HS256']


def encode_payload(payload: dict):
    return encode(
        payload=payload,
        algorithm=algorithms[0],
        key=SECRET_KEY.hex()
    )


def get_payload(user_id: int, code_id: int, host: str = None, client: str = None) -> dict:
    if host is None:
        host = request.host

    if client is None:
        client = request.origin

    return {
        "user_id": user_id,
        "code_id": code_id,
        "time": {
            "a": int(timestamp()),
            "b": int(timestamp()) + timedelta(hours=2, minutes=30).seconds,
        },
        "host": host,
        "client": client
    }
