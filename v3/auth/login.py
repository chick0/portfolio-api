from re import compile
from random import choices
from hashlib import sha512
from datetime import datetime
from datetime import timedelta

from fastapi import APIRouter
from fastapi import Request
from fastapi import HTTPException
from fastapi import status as _

from sql import get_session
from sql.models import User
from sql.models import LoginRequest
from mail.utils import send_mail
from v3.auth.models import LoginRequest as _LoginRequest
from v3.auth.models import LoginResponse

router = APIRouter()
re = compile(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)')
HTTP_201_CREATED = _.HTTP_201_CREATED


@router.post(
    "/login",
    description="비밀번호로 로그인합니다.",
    response_model=LoginResponse,
    status_code=HTTP_201_CREATED
)
async def login_with_password(request: _LoginRequest, ctx: Request):
    if re.match(request.email) is None:
        raise HTTPException(
            status_code=400,
            detail={
                "alert": "이메일이 올바르지 않습니다."
            }
        )

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

    login_request: LoginRequest = session.query(LoginRequest).filter_by(
        owner_id=user.id
    ).filter(
        LoginRequest.expired_date >= datetime.now()
    ).first()

    if login_request is not None:
        raise HTTPException(
            status_code=403,
            detail={
                "alert": "다른 세션에서 로그인을 시도하고 있습니다."
            }
        )

    login_request = LoginRequest()
    login_request.owner_id = user.id
    login_request.code = "".join(choices(['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'], k=6))
    login_request.ip = ctx.client.host
    login_request.expired_date = datetime.now() + timedelta(minutes=3)

    session.add(login_request)
    session.commit()

    user_id = user.id
    request_id = login_request.id

    send_mail(
        email=user.email,
        code=login_request.code,
        ip=ctx.client.host
    )

    session.close()

    return LoginResponse(
        user_id=user_id,
        request_id=request_id,
    )
