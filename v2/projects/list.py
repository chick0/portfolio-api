from math import ceil

from fastapi import APIRouter
from fastapi import HTTPException
from pydantic import BaseModel

from sql import get_session
from sql.models import Project

router = APIRouter(
    prefix="/list"
)

ITEM_PER_PAGE = 20


class ProjectPreview(BaseModel):
    uuid: str
    title: str
    date: str
    tags: list[str]


class PageData(BaseModel):
    this: int
    max: int


class ProjectList(BaseModel):
    projectList: list[ProjectPreview]
    page: PageData


@router.get(
    "/page",
    description="프로젝트 목록을 불러옵니다.",
    response_model=ProjectList
)
async def show_list(page: int = 1):
    session = get_session()

    length = session.query(Project).count()
    max_page = ceil(length / ITEM_PER_PAGE)

    if page > max_page or page <= 0:
        raise HTTPException(
            status_code=400,
            detail={
                "alert": "요청하신 페이지를 찾을 수 없습니다.",
                "max": max_page
            }
        )

    return ProjectList(
        projectList=[
            ProjectPreview(
                uuid=x.uuid,
                title=x.title,
                date=x.date.strftime("%Y년 %m월 %d일"),
                tags=[x.strip() for x in x.tag.split(",")]
            ) for x in session.query(Project).order_by(
                Project.date.desc()
            ).with_entities(
                Project.uuid,
                Project.title,
                Project.date,
                Project.tag,
            ).offset(ITEM_PER_PAGE * (page - 1)).limit(ITEM_PER_PAGE).all()
        ],
        page=PageData(
            this=page,
            max=max_page,
        )
    )


@router.get(
    "/tags",
    description="태그와 관련된 프로젝트 목록을 불러옵니다.",
    response_model=ProjectList
)
async def show_list_with_tags(tags: str, page: int = 1):
    session = get_session()
    return []
