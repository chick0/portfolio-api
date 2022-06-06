from fastapi import APIRouter

router = APIRouter()


@router.get(
    "/{project_id}",
    description="프로젝트 정보를 불러옵니다."
)
async def show_detail(project_id: str):
    return {}


@router.put(
    "/{project_id}",
    description="프로젝트 정보를 수정합니다."
)
async def edit(project_id: str):
    return {}


@router.delete(
    "/{project_id}",
    description="프로젝트 정보를 삭제합니다."
)
async def delete(project_id: str):
    return {}
