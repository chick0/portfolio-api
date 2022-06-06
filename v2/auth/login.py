from fastapi import APIRouter

router = APIRouter(
    prefix="/login"
)


@router.post(
    "",
    description="이메일과 비밀번호로 로그인을 진행합니다."
)
async def login():
    return {}


@router.post(
    "/code",
    description="이메일로 전송된 인증 코드를 검증합니다."
)
async def code_verify():
    return {}
