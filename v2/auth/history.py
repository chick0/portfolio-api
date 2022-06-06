from fastapi import APIRouter

router = APIRouter(
    prefix="/history"
)


@router.get(
    "/login",
    description="로그인 기록을 조회합니다."
)
async def login_history():
    return {}
