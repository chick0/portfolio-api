from uuid import uuid4
from datetime import datetime

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import HTTPBearer
from pydantic import BaseModel

from sql import get_session
from sql.models import Project
from v2.utils import parse_token

router = APIRouter()

auth_scheme = HTTPBearer()


class ProjectCreated(BaseModel):
    uuid: str


class ProjectRequest(BaseModel):
    title: str
    date: str  # YYYY-MM-DD
    tag: str
    web: str
    github: str
    a: str
    b: str
    c: str


@router.post(
    "/create",
    description="새로운 프로젝트를 생성합니다.",
    response_model=ProjectCreated
)
async def create_project(request: ProjectRequest, token=Depends(auth_scheme)):
    parse_token(token=token)

    project = Project()
    project.uuid = uuid4().__str__()
    project.title = request.title.strip()
    try:
        project.date = datetime.strptime(request.date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail={
                "alert": "날짜 형식이 올바르지 않습니다."
            }
        )

    project.tag = request.tag
    project.web = request.web
    project.github = request.github
    project.a = request.a
    project.b = request.b
    project.c = request.c

    session = get_session()
    session.add(project)
    session.commit()

    return ProjectCreated(
        uuid=project.uuid
    )
