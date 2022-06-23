from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import HTTPBearer

from sql import get_session
from sql.models import Project
from sql.models import Button
from utils.token import parse_token
from v3.project.models import ProjectDeleteStatus

router = APIRouter()
auth_scheme = HTTPBearer()


@router.delete(
    "/{project_uuid}",
    description="프로젝트를 삭제합니다.",
    response_model=ProjectDeleteStatus
)
async def project_delete(project_uuid: str, token=Depends(auth_scheme)):
    parse_token(token=token)
    session = get_session()

    deleted = session.query(Project).filter_by(
        uuid=project_uuid
    ).delete()

    session.query(Button).filter_by(
        project_uuid=project_uuid
    ).delete()

    session.commit()
    session.close()

    return ProjectDeleteStatus(
        status=deleted == 1
    )
