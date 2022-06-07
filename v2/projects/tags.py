from math import ceil

from fastapi import APIRouter
from fastapi import HTTPException
from pydantic import BaseModel

from sql import get_session
from sql.models import Project

from .index import ITEM_PER_PAGE
from .index import ProjectPreview
from .index import PageData
from .index import ProjectList

router = APIRouter()


@router.get(
    "/tags",
    description="태그와 관련된 프로젝트 목록을 불러옵니다.",
    response_model=ProjectList
)
async def show_list_with_tags(tags: str, page: int = 1):
    return []
