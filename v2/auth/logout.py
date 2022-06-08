from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import HTTPBearer
from pydantic import BaseModel

from sql import get_session
from sql.models import LoginSession
from v2.utils import parse_token

router = APIRouter(
    prefix="/logout"
)

auth_scheme = HTTPBearer()


class LogoutResult(BaseModel):
    status: bool


@router.delete(
    "",
    description="세션을 만료시키고 로그아웃 합니다.",
    response_model=LogoutResult
)
async def session_logout(session_id: int = None, token=Depends(auth_scheme)):
    payload = parse_token(token=token)
    session = get_session()

    login_session: LoginSession = session.query(LoginSession).filter_by(
        id=session_id if session_id is not None else payload.session_id,
        owner_id=payload.user_id,
    ).first()

    if login_session is None:
        raise HTTPException(
            status_code=404,
            detail={
                "alert": "해당 로그인 세션을 찾지 못했습니다.",
            }
        )

    if login_session.revoked:
        raise HTTPException(
            status_code=404,
            detail={
                "alert": "해당 세션은 이미 만료된 세션입니다.",
            }
        )

    login_session.revoked = True
    session.commit()

    return LogoutResult(
        status=True
    )
