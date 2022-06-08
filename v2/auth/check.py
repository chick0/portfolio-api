from datetime import datetime

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends
from fastapi.security import HTTPBearer
from pydantic import BaseModel

from v2.utils import parse_token

router = APIRouter(
    prefix="/check"
)

auth_scheme = HTTPBearer()


class TokenCheckResponse(BaseModel):
    status: bool
    ttl: int


@router.get(
    "/token",
    description="인증 토큰이 유요한지 검사합니다.",
    response_model=TokenCheckResponse
)
async def check_token(token=Depends(auth_scheme)):
    try:
        payload = parse_token(token=token)
        ttl = (datetime.now() - datetime.fromtimestamp(payload.exp)).seconds
    except HTTPException:
        payload = None
        ttl = 0

    return TokenCheckResponse(
        status=payload is not None,
        ttl=ttl
    )
