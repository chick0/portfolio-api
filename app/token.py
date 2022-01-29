from time import time as timestamp
from collections import namedtuple

from flask import request
from jwt import decode
from jwt.exceptions import InvalidSignatureError

from app import auth
from app.secret_key import SECRET_KEY
from app.config import get_config

ERR = namedtuple("ERR", "message status")
TIME = namedtuple("TIME", "a b")
TOKEN = namedtuple(
    "TOKEN",
    [
        "id",
        "time",
        "host",
        "client",
        "type",
    ]
)


def get_token(id_: str,
              host: str = None, client: str = None, type_: str = None, time: int = 6 * 3600) -> dict:
    if host is None:
        host = request.host

    if client is None:
        client = request.origin

    if type_ is None:
        type_ = "github"

    return TOKEN(
        id=id_,
        time=TIME(
            a=int(timestamp()),
            b=int(timestamp()) + time,
        )._asdict(),
        host=host,
        client=client,
        type=type_
    )._asdict()


def parse(token: dict) -> TOKEN:
    tk = TOKEN(**token)
    tt = TIME(**tk.time)

    now = timestamp()
    if tt.a < now < tt.b:
        return tk
    else:
        raise TimeoutError("토큰 만료됨")


def check() -> ERR or None:
    try:
        authorization = request.headers.get("authorization")
        tp, token = authorization.split(" ")

        if tp != "Bearer":
            raise TypeError
    except (ValueError, AttributeError):
        return ERR(
            message="인증 토큰이 없습니다.",
            status=400
        )
    except TypeError:
        return ERR(
            message="요청 형식이 올바르지 않습니다.",
            status=400
        )

    try:
        token = decode(
            jwt=token,
            key=SECRET_KEY.hex(),
            algorithms=["HS256"]
        )
    except (InvalidSignatureError, Exception):
        return ERR(
            message="인증키가 올바르지 않습니다",
            status=400
        )

    try:
        token = parse(token=token)
    except TypeError:
        return ERR(
            message="토큰 형식이 올바르지 않습니다.",
            status=400
        )
    except TimeoutError:
        return ERR(
            message="만료된 인증토큰 입니다.",
            status=401
        )

    if token.host != request.host:
        return ERR(
            message="토큰을 생성한 API 서버가 다릅니다.",
            status=403
        )

    if token.client != request.origin:
        return ERR(
            message="토큰을 생성한 클라이언트가 다릅니다.",
            status=403
        )

    if token.type not in auth.__all__:
        return ERR(
            message="토큰을 생성한 서비스는 허용된 서비스가 아닙니다.",
            status=400
        )

    id_name = token.type + "_id"
    cid = getattr(get_config("User"), id_name)

    if str(token.id) != cid:
        return ERR(
            message="해당 유저는 접근권한이 없습니다.",
            status=403
        )

    return None
