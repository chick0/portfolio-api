from time import time as timestamp

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


def get_payload(id: int, host: str = None, client: str = None, time: int = 6 * 3600) -> dict:
    if host is None:
        host = request.host

    if client is None:
        client = request.origin

    return {
        "id": id,
        "time": {
            "a": int(timestamp()),
            "b": int(timestamp()) + time,
        },
        "host": host,
        "client": client
    }
