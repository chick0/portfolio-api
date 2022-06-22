from uuid import uuid4
from datetime import datetime

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import HTTPBearer

from sql import get_session
from sql.models import Project
from utils.token import parse_token
from v3.project.models import ProjectRequest
from v3.project.models import ProjectCreated

router = APIRouter()
auth_scheme = HTTPBearer()


@router.post(
    "/create",
    description="새로운 프로젝트를 생성합니다.",
    response_model=ProjectCreated
)
async def create_project(request: ProjectRequest, token=Depends(auth_scheme)):
    parse_token(token=token)

    uuid = uuid4().__str__()

    project = Project()
    project.uuid = uuid
    project.title = request.title.strip()
    project.tag = request.tag
    project.web = request.web
    project.github = request.github
    project.a = request.a
    project.b = request.b
    project.c = request.c

    try:
        project.date = datetime.strptime(request.date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail={
                "alert": "날짜 형식이 올바르지 않습니다."
            }
        )

    session = get_session()
    session.add(project)
    session.commit()
    session.close()

    return ProjectCreated(
        uuid=uuid
    )
