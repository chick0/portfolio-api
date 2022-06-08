from random import choices
from hashlib import sha512
from datetime import datetime
from datetime import timedelta

from fastapi import APIRouter
from fastapi import Request
from fastapi import HTTPException
from fastapi import Depends
from fastapi.security import HTTPBearer
from pydantic import BaseModel

from sql import get_session
from sql.models import User
from sql.models import Code
from sql.models import LoginSession
from v2.utils import create_token
from v2.utils import parse_token
from mail.utils import send_mail

router = APIRouter(
    prefix="/login"
)

auth_scheme = HTTPBearer()


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    user_id: int
    request_id: int


class VerifyRequest(BaseModel):
    user_id: int
    request_id: int
    code: str


class TokenResponse(BaseModel):
    token: str


@router.post(
    "",
    description="이메일과 비밀번호로 로그인을 진행합니다.",
    response_model=LoginResponse
)
async def login_with_password(request: LoginRequest, ctx: Request):
    session = get_session()
    user: User = session.query(User).filter_by(
        email=request.email,
        password=sha512(request.password.encode()).hexdigest()
    ).first()

    if user is None:
        raise HTTPException(
            status_code=403,
            detail={
                "alert": "이메일 또는 비밀번호가 올바르지 않습니다."
            }
        )

    code: Code = session.query(Code).filter_by(
        owner_id=user.id
    ).filter(
        Code.expired_date >= datetime.now()
    ).first()

    if code is not None:
        raise HTTPException(
            status_code=403,
            detail={
                "alert": "다른 세션에서 로그인을 시도하고 있습니다."
            }
        )

    code = Code()
    code.owner_id = user.id
    code.code = "".join(choices(['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'], k=6))
    code.ip = ctx.client.host
    code.expired_date = datetime.now() + timedelta(minutes=3)

    session.add(code)
    session.commit()

    send_mail(
        email=user.email,
        code=code.code,
        ip=ctx.client.host
    )

    return LoginResponse(
        user_id=user.id,
        request_id=code.id
    )


@router.post(
    "/code",
    description="이메일로 전송된 인증 코드를 검증합니다.",
    response_model=TokenResponse
)
async def code_verify(request: VerifyRequest, ctx: Request):
    session = get_session()
    code: Code = session.query(Code).filter_by(
        id=request.request_id,
        owner_id=request.user_id,
        code=request.code
    ).filter(
        Code.expired_date >= datetime.now()
    ).first()

    if code is None:
        raise HTTPException(
            status_code=403,
            detail={
                "alert": "인증 코드가 올바르지 않습니다."
            }
        )

    login_session = LoginSession()
    login_session.owner_id = code.owner_id
    login_session.ip = ctx.client.host
    login_session.revoked = False

    session.add(login_session)
    session.delete(code)
    session.commit()

    return TokenResponse(
        token=create_token(
            user_id=login_session.owner_id,
            session_id=login_session.id,
        )
    )


@router.post(
    "/renew",
    description="발급된 인증 토큰을 연장합니다.",
    response_model=TokenResponse
)
async def token_renew(token=Depends(auth_scheme)):
    payload = parse_token(token=token)
    return TokenResponse(
        token=create_token(
            user_id=payload.user_id,
            session_id=payload.session_id
        )
    )
