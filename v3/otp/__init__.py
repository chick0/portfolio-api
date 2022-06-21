from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends
from fastapi import status as _
from fastapi.security import HTTPBearer
from pyotp import random_base32
from pyotp import TOTP

from sql import get_session
from sql.models import User
from utils.token import parse_token
from v3.otp.models import OTPResult
from v3.otp.models import OTPDeleteStatus

router = APIRouter()
auth_scheme = HTTPBearer()
HTTP_201_CREATED = _.HTTP_201_CREATED


@router.post(
    "/otp",
    description="OTP 시크릿을 생성합니다.",
    response_model=OTPResult,
    status_code=HTTP_201_CREATED
)
async def create_otp_secret(token=Depends(auth_scheme)):
    payload = parse_token(token=token)
    session = get_session()

    user: User = session.query(User).filter_by(
        id=payload.user_id
    ).first()

    email = user.email

    if user is None:
        raise HTTPException(
            status_code=400,
            detail={
                "alert": "해당 유저를 찾을 수 없습니다."
            }
        )

    if user.otp is not None:
        raise HTTPException(
            status_code=400,
            detail={
                "alert": "OTP가 이미 설정되어있습니다."
            }
        )

    secret = random_base32()
    otp = TOTP(secret)

    user.otp = secret
    session.commit()
    session.close()

    return OTPResult(
        url=otp.provisioning_uri(
            name=email,
            issuer_name="my portfolio api",
        )
    )


@router.delete(
    "/otp",
    description="OTP 시크릿을 삭제합니다.",
    response_model=OTPDeleteStatus,
)
async def delete_otp_secret(token=Depends(auth_scheme)):
    payload = parse_token(token=token)
    session = get_session()

    user: User = session.query(User).filter_by(
        id=payload.user_id
    ).first()

    if user is None:
        raise HTTPException(
            status_code=400,
            detail={
                "alert": "해당 유저를 찾을 수 없습니다."
            }
        )

    if user.otp is None:
        raise HTTPException(
            status_code=400,
            detail={
                "alert": "OTP가 설정되어있지 않습니다."
            }
        )

    user.otp = None

    session.commit()
    session.close()

    return OTPDeleteStatus(
        status=True
    )
