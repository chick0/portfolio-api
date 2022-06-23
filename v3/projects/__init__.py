from math import ceil

from fastapi import APIRouter
from fastapi import HTTPException
from sqlalchemy import and_

from sql import get_session
from sql.models import Project
from v3.projects.utils import to_pretty
from v3.projects.models import ProjectPreview
from v3.projects.models import ProjectList
from v3.projects.models import PageData

ITEM_PER_PAGE = 20
router = APIRouter()


@router.get(
    "/projects",
    description="프로젝트 목록을 불러옵니다.",
    response_model=ProjectList
)
async def project_list(page: int = 1):
    with get_session() as session:
        length = session.query(Project).count()
        max_page = ceil(length / ITEM_PER_PAGE)

        if length == 0:
            raise HTTPException(
                status_code=400,
                detail={
                    "alert": "등록된 프로젝트가 없습니다."
                }
            )

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
                    date=to_pretty(
                        date=x.date
                    ),
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
    "/projects/tags",
    description="프로젝트 목록을 불러옵니다.",
    response_model=ProjectList
)
async def project_list_with_tags(tags: str, page: int = 1):
    tags = [
        x
        for x in [x.strip() for x in tags.split(",")]
        if len(x) != 0
    ]

    if len(tags) == 0:
        raise HTTPException(
            status_code=400,
            detail={
                "alert": "검색할 태그가 없습니다."
            }
        )

    tag_filter = and_(
        Project.tag.like(f"%{x}%")
        for x in tags
    )

    with get_session() as session:
        length = session.query(Project).filter(tag_filter).count()
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
                    date=to_pretty(
                        date=x.date
                    ),
                    tags=[x.strip() for x in x.tag.split(",")]
                ) for x in session.query(Project).order_by(
                    Project.date.desc()
                ).with_entities(
                    Project.uuid,
                    Project.title,
                    Project.date,
                    Project.tag,
                ).filter(tag_filter).offset(ITEM_PER_PAGE * (page - 1)).limit(ITEM_PER_PAGE).all()
            ],
            page=PageData(
                this=page,
                max=max_page,
            )
        )
