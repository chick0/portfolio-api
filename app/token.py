from time import time as timestamp

from flask import request
from flask import jsonify
from flask import Response
from jwt import encode
from jwt import decode
from jwt.exceptions import InvalidSignatureError

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


def check() -> Response or None:
    try:
        authorization = request.headers.get("authorization")
        tp, token = authorization.split(" ")

        if tp != "Bearer":
            raise TypeError
    except (ValueError, AttributeError):
        return jsonify(
            message="인증 토큰이 없습니다.",
            status=400
        )
    except TypeError:
        return jsonify(
            message="요청 형식이 올바르지 않습니다.",
            status=400
        )

    try:
        token = decode(
            jwt=token,
            key=SECRET_KEY.hex(),
            algorithms=algorithms
        )
    except (InvalidSignatureError, Exception):
        return jsonify(
            message="인증 토큰 검증에 실패했습니다.",
            status=400
        )

    try:
        if token['time']['a'] < round(timestamp()) <= token['time']['b']:
            # 만료되지 않은 토큰
            pass
        else:
            return jsonify(
                message="만료된 인증토큰 입니다.",
                status=401
            )

        if token['host'] != request.host:
            return jsonify(
                message="토큰을 생성한 API 서버가 다릅니다.",
                status=403
            )

        if token['client'] != request.origin:
            return jsonify(
                message="토큰을 생성한 클라이언트가 다릅니다.",
                status=403
            )
    except KeyError:
        return jsonify(
            message="토큰 형식이 올바르지 않습니다.",
            status=400
        )

    return None
