from datetime import datetime

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import HTTPBearer

from sql import get_session
from sql.models import LoginSession
from utils.token import parse_token
from utils.token import create_token
from v3.auth.models import TokenStatus
from v3.auth.models import TokenResponse
from v3.auth.models import TokenRevokeStatus

router = APIRouter()
auth_scheme = HTTPBearer()


@router.get(
    "/token",
    description="인증 토큰의 상태를 확인합니다.",
    response_model=TokenStatus
)
async def check_token(token=Depends(auth_scheme)):
    try:
        payload = parse_token(token=token)
        ttl = (datetime.now() - datetime.fromtimestamp(payload.exp)).seconds
    except HTTPException:
        payload = None
        ttl = 0

    return TokenStatus(
        status=payload is not None,
        ttl=ttl
    )


@router.patch(
    "/token",
    description="인증 토큰을 재발급 합니다.",
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


@router.delete(
    "/token",
    description="인증 토큰을 만료 시킵니다.",
    response_model=TokenRevokeStatus
)
async def revoke_token(token=Depends(auth_scheme)):
    payload = parse_token(token=token)
    session = get_session()

    login_session: LoginSession = session.query(LoginSession).filter_by(
        id=payload.session_id,
        owner_id=payload.user_id
    ).first()

    if login_session is not None:
        login_session.revoked = True

    session.commit()
    session.close()

    return TokenRevokeStatus(
        status=True
    )
