from uuid import uuid4

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status as _
from fastapi.security import HTTPBearer

from sql import get_session
from sql.models import Project
from sql.models import Button
from utils.token import parse_token
from v3.buttons.models import ButtonRequest
from v3.buttons.models import ButtonResponse

HTTP_201_CREATED = _.HTTP_201_CREATED
router = APIRouter()
auth_scheme = HTTPBearer()


@router.post(
    "/{project_uuid}",
    description="새로운 버튼을 생성합니다.",
    response_model=ButtonResponse,
    status_code=HTTP_201_CREATED
)
async def create_button(project_uuid: str, request: ButtonRequest, token=Depends(auth_scheme)):
    parse_token(token=token)
    session = get_session()

    project: Project = session.query(Project).filter_by(
        uuid=project_uuid
    ).first()

    if project is None:
        raise HTTPException(
            status_code=400,
            detail={
                "alert": "해당 프로젝트는 등록된 프로젝트가 아닙니다."
            }
        )

    uuid = uuid4().__str__()

    button = Button()
    button.uuid = uuid
    button.project_uuid = project_uuid
    button.text = request.text.strip()
    button.url = request.url.strip()
    button.color = request.color.strip()

    session.add(button)
    session.commit()
    session.close()

    return ButtonResponse(
        uuid=uuid,
        text=request.text.strip(),
        url=request.url.strip(),
        color=request.color.strip()
    )
