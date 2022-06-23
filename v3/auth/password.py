from hashlib import sha512

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends
from fastapi.security import HTTPBearer

from sql import get_session
from sql.models import User
from utils.token import parse_token
from v3.auth.models import PasswordUpdateRequest
from v3.auth.models import PasswordUpdateStatus

router = APIRouter()
auth_scheme = HTTPBearer()


@router.patch(
    "/password",
    description="비밀번호를 변경합니다.",
    response_model=PasswordUpdateStatus
)
async def password_update(request: PasswordUpdateRequest, token=Depends(auth_scheme)):
    payload = parse_token(token=token)
    session = get_session()

    user: User = session.query(User).filter_by(
        id=payload.user_id,
        password=sha512(request.old_password.encode()).hexdigest()
    ).first()

    if user is None:
        raise HTTPException(
            status_code=403,
            detail={
                "alert": "비밀번호가 일치하지 않습니다."
            }
        )

    user.password = sha512(request.new_password.encode()).hexdigest()
    session.commit()
    session.close()

    return PasswordUpdateStatus(
        status=True
    )
