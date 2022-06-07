from datetime import datetime
from datetime import timedelta

from fastapi import HTTPException
from fastapi.security.http import HTTPAuthorizationCredentials
from pydantic import BaseModel
from jwt import encode
from jwt import decode

from key import get
from sql import get_session
from sql.models import LoginSession


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
            "exp": round((datetime.now() + timedelta(hours=2, minutes=30)).timestamp())
        },
        key=get(),
        algorithm=algorithms[0]
    )


def parse_token(token: HTTPAuthorizationCredentials) -> TokenPayload:
    payload = TokenPayload(**decode(
        jwt=token.credentials,
        key=get(),
        algorithms=algorithms
    ))

    if datetime.fromtimestamp(payload.exp) < datetime.now():
        raise HTTPException(
            status_code=401,
            detail={
                "alert": "인증 토큰이 만료되었습니다."
            }
        )

    session = get_session()
    login_session: LoginSession = session.query(LoginSession).filter_by(
        id=payload.session_id,
        owner_id=payload.user_id,
        revoked=False,
    ).first()

    if login_session is None:
        raise HTTPException(
            status_code=401,
            detail={
                "alert": "인증 세션이 만료되었습니다."
            }
        )

    return payload
