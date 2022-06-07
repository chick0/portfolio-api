from datetime import datetime
from datetime import timedelta

from fastapi.security.http import HTTPAuthorizationCredentials
from pydantic import BaseModel
from jwt import encode
from jwt import decode

from key import get


algorithms = ['HS256']


class TokenPayload(BaseModel):
    user_id: int
    session_id: int
    exp: int


def create_token(user_id: int, session_id: int) -> str:
    return encode(
        payload={
            "user_id": user_id,
            "session_id": session_id,
            "exp": (datetime.now() + timedelta(hours=2, minutes=30)).timestamp()
        },
        key=get(),
        algorithm=algorithms[0]
    )


def parse_token(token: HTTPAuthorizationCredentials) -> dict:
    payload = decode(token.credentials)

    return {}
