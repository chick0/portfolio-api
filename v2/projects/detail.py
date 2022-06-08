from datetime import datetime

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends
from fastapi.security import HTTPBearer
from pydantic import BaseModel

from sql import get_session
from sql.models import Project
from v2.utils import parse_token

router = APIRouter()

auth_scheme = HTTPBearer()


class Date(BaseModel):
    timestamp: int
    pretty: str
    ymd: str


def to_date(date: datetime) -> Date:
    return Date(
        timestamp=round(date.timestamp()),
        pretty=date.strftime("%Y년 %m월 %d일"),
        ymd=date.strftime("%Y-%m-%d")
    )


class ProjectDetail(BaseModel):
    uuid: str
    title: str
    date: Date
    tags: list[str]
    web: str
    github: str
    a: str  # 기획 의도
    b: str  # 특징
    c: str  # 느낀점


class ProjectEditRequest(BaseModel):
    uuid: str
    title: str
    date: str   # YYYY-MM-DD
    tags: str
    web: str
    github: str
    a: str  # 기획 의도
    b: str  # 특징
    c: str  # 느낀점


class ProjectUpdateResult(BaseModel):
    status: bool


@router.get(
    "/{project_id}",
    description="프로젝트 정보를 불러옵니다.",
    response_model=ProjectDetail
)
async def show_detail(project_id: str):
    session = get_session()

    project: Project = session.query(Project).filter_by(
        uuid=project_id
    ).first()

    if project is None:
        raise HTTPException(
            status_code=404,
            detail={
                "alert": "해당 프로젝트를 찾지 못 했습니다."
            }
        )

    return ProjectDetail(
        uuid=project.uuid,
        title=project.title,
        date=to_date(
            date=project.date
        ),
        tags=[
            x
            for x in [x.strip() for x in project.tag.split(",")]
            if len(x) != 0
        ],
        web=project.web,
        github=project.github,
        a=project.a,
        b=project.b,
        c=project.c
    )


@router.put(
    "/{project_id}",
    description="프로젝트 정보를 수정합니다.",
    response_model=ProjectUpdateResult
)
async def edit(project_id: str, request: ProjectEditRequest, token=Depends(auth_scheme)):
    payload = parse_token(token=token)
    session = get_session()

    project: Project = session.query(Project).filter_by(
        uuid=project_id
    ).first()

    if payload is None:
        raise HTTPException(
            status_code=404,
            detail={
                "alert": "해당 프로젝트를 찾지 못 했습니다."
            }
        )

    try:
        date = datetime.strptime(request.date, "%Y-%m-%d")
    except ValueError:
        date = project.date

    project.title = request.title
    project.date = date
    project.tag = request.tags
    project.web = request.web
    project.github = request.github

    project.a = request.a
    project.b = request.b
    project.c = request.c

    session.commit()

    return ProjectUpdateResult(
        status=True,
    )


@router.delete(
    "/{project_id}",
    description="프로젝트 정보를 삭제합니다.",
    response_model=ProjectUpdateResult
)
async def delete(project_id: str, token=Depends(auth_scheme)):
    payload = parse_token(token=token)
    session = get_session()

    deleted = session.query(Project).filter_by(
        uuid=project_id
    ).delete()

    session.commit()

    return ProjectUpdateResult(
        status=deleted == 1
    )
