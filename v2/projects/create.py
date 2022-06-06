from fastapi import APIRouter

router = APIRouter()


@router.post(
    "/create",
    description="새로운 프로젝트를 생성합니다."
)
async def create_project():
    return {}
