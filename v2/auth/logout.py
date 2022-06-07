from fastapi import APIRouter
from fastapi import Depends
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
    pass


@router.delete(
    "",
    description="세션을 삭제하고 로그아웃 합니다.",
    response_model=LogoutResult
)
async def logout(token=Depends(auth_scheme)):
    payload = parse_token(token=token)
    session = get_session()

    login_session: LoginSession = session.query(LoginSession).filter_by(
        id=payload.session_id,
        owner_id=payload.user_id
    ).first()

    login_session.revoked = True
    session.commit()

    return LogoutResult()
