from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import HTTPBearer
from pydantic import BaseModel

from sql import get_session
from sql.models import LoginSession
from v2.utils import parse_token
from v2.projects.detail import Date
from v2.projects.detail import to_date

router = APIRouter(
    prefix="/history"
)

auth_scheme = HTTPBearer()


class LoginHistory(BaseModel):
    id: int
    ip: str
    creation_date: Date
    revoked: bool
    same: bool


class LoginHistoryList(BaseModel):
    historyList: list[LoginHistory]


@router.get(
    "/login",
    description="로그인 기록을 조회합니다.",
    response_model=LoginHistoryList
)
async def login_history(token=Depends(auth_scheme)):
    payload = parse_token(token=token)
    session = get_session()
    return {
        "historyList": [
            {
                "id": x.id,
                "ip": x.ip,
                "creation_date": to_date(
                    date=x.creation_date
                ),
                "revoked": x.revoked,
                "same": x.id == payload.session_id,
            } for x in session.query(LoginSession).filter_by(
                owner_id=payload.user_id,
            ).order_by(
                LoginSession.id.desc()
            )
        ]
    }
