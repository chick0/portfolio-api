from fastapi import APIRouter

router = APIRouter(
    prefix="/index"
)


@router.get(
    "",
    description="프로젝트 목록을 불러옵니다."
)
async def show_list(page_id: int):
    return []


@router.get(
    "/tags",
    description="태그와 관련된 프로젝트 목록을 불러옵니다."
)
async def show_list_with_tags(tags: str, page_id: int):
    return []
