from datetime import datetime

from fastapi import APIRouter
from fastapi import Request
from fastapi import HTTPException
from fastapi import status as _

from sql import get_session
from sql.models import User
from sql.models import LoginRequest
from sql.models import LoginSession
from utils.token import create_token
from v3.auth.models import VerifyRequest
from v3.auth.models import TokenResponse

router = APIRouter(prefix="/verify")
HTTP_201_CREATED = _.HTTP_201_CREATED


@router.post(
    "/email",
    description="",
    response_model=TokenResponse,
    status_code=HTTP_201_CREATED
)
async def verify_with_email(request: VerifyRequest, ctx: Request):
    session = get_session()
    login_request: LoginRequest = session.query(LoginRequest).filter_by(
        id=request.request_id,
        owner_id=request.user_id,
        code=request.token.replace(" ", "")
    ).filter(
        LoginRequest.expired_date >= datetime.now()
    ).first()

    if login_request is None:
        raise HTTPException(
            status_code=400,
            detail={
                "alert": "인증 코드가 올바르지 않습니다."
            }
        )

    login_session = LoginSession()
    login_session.owner_id = request.user_id
    login_session.ip = ctx.client.host
    login_session.revoked = False

    session.add(login_session)
    session.delete(login_request)
    session.commit()

    session_id = login_session.id
    session.close()

    return TokenResponse(
        token=create_token(
            user_id=request.user_id,
            session_id=session_id
        )
    )


@router.post(
    "/otp",
    description="",
    response_model=TokenResponse,
    status_code=HTTP_201_CREATED
)
async def verify_with_otp_token(request: VerifyRequest, ctx: Request):
    session = get_session()
    login_request: LoginRequest = session.query(LoginRequest).filter_by(
        id=request.request_id,
        owner_id=request.user_id,
    ).filter(
        LoginRequest.expired_date >= datetime.now()
    ).first()

    if login_request is None:
        raise HTTPException(
            status_code=400,
            detail={
                "alert": "인증 요청이 올바르지 않습니다."
            }
        )

    user: User = session.query(User).filter_by(
        id=request.user_id
    ).with_entities(
        User.otp
    ).first()

    if user is None:
        raise HTTPException(
            status_code=400,
            detail={
                "alert": "등록된 유저가 아닙니다."
            }
        )

    if user.otp is None:
        raise HTTPException(
            status_code=400,
            detail={
                "alert": "OTP 설정이 완료되지 않았습니다."
            }
        )

    login_session = LoginSession()
    login_session.owner_id = request.user_id
    login_session.ip = ctx.client.host
    login_session.revoked = False

    session.add(login_session)
    session.delete(login_request)
    session.commit()

    session_id = login_session.id
    session.close()

    return TokenResponse(
        token=create_token(
            user_id=request.user_id,
            session_id=session_id
        )
    )
