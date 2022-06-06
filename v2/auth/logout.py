from fastapi import APIRouter

router = APIRouter(
    prefix="/logout"
)


@router.delete(
    "",
    description="세션을 삭제하고 로그아웃 합니다."
)
async def logout():
    return {}
