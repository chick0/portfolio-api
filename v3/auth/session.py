from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import HTTPBearer

from sql import get_session
from sql.models import LoginSession
from utils.token import parse_token
from v3.auth.models import Session
from v3.auth.models import SessionList
from v3.auth.models import SessionRevokeStatus
from v3.storage.utils import to_date

router = APIRouter()
auth_scheme = HTTPBearer()


@router.get(
    "/session",
    description="전체 세션 목록을 가져옵니다.",
    response_model=SessionList
)
async def get_session_list(token=Depends(auth_scheme)):
    payload = parse_token(token=token)
    with get_session() as session:
        return SessionList(
            sessionList=[
                Session(
                    id=x.id,
                    ip=x.ip,
                    creation_date=to_date(
                        date=x.creation_date
                    ),
                    revoked=x.revoked,
                    same=x.id == payload.session_id
                ) for x in session.query(LoginSession).filter_by(
                    owner_id=payload.user_id,
                ).order_by(
                    LoginSession.id.desc()
                ).all()
            ]
        )


@router.delete(
    "/session/{session_id}",
    description="해당 세션을 만료 시킵니다.",
    response_model=SessionRevokeStatus
)
async def revoke_session(session_id: int, token=Depends(auth_scheme)):
    payload = parse_token(token=token)
    session = get_session()

    login_session: LoginSession = session.query(LoginSession).filter_by(
        id=session_id,
        owner_id=payload.user_id
    ).first()

    if login_session is None:
        session.close()

        return SessionRevokeStatus(
            status=False
        )

    login_session.revoked = True

    session.commit()
    session.close()

    return SessionRevokeStatus(
        status=True
    )


@router.delete(
    "/session",
    description="등록된 모든 세션을 삭제합니다.",
    response_model=SessionRevokeStatus
)
async def delete_all_session(token=Depends(auth_scheme)):
    payload = parse_token(token=token)
    session = get_session()

    session.query(LoginSession).filter_by(
        owner_id=payload.user_id
    ).delete()

    session.commit()
    session.close()

    return SessionRevokeStatus(
        status=True
    )
