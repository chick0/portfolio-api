from datetime import datetime

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import HTTPBearer

from sql import get_session
from sql.models import Project
from utils.token import parse_token
from v3.project.models import ProjectRequest
from v3.project.models import ProjectEditResult

router = APIRouter()
auth_scheme = HTTPBearer()


@router.patch(
    "/{project_uuid}",
    description="프로젝트 정보를 수정합니다.",
    response_model=ProjectEditResult
)
async def project_detail(project_uuid: str, request: ProjectRequest, token=Depends(auth_scheme)):
    parse_token(token=token)
    session = get_session()

    project: Project = session.query(Project).filter_by(
        uuid=project_uuid
    ).first()

    if project is None:
        raise HTTPException(
            status_code=404,
            detail={
                "alert": "해당 프로젝트를 찾지 못했습니다."
            }
        )

    try:
        date = datetime.strptime(request.date, "%Y-%m-%d")
    except ValueError:
        date = project.date

    project.title = request.title
    project.date = date
    project.tag = request.tag
    project.web = request.web
    project.github = request.github

    project.a = request.a
    project.b = request.b
    project.c = request.c

    session.commit()
    session.close()

    return ProjectEditResult(
        result=True
    )
