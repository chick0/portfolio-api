from fastapi import APIRouter

from sql import get_session
from sql.models import Button
from v3.buttons.models import ButtonResponse
from v3.buttons.models import ButtonList

router = APIRouter()


@router.get(
    "/{project_uuid}",
    description="등록된 버튼을 불러옵니다.",
    response_model=ButtonList
)
async def get_button(project_uuid: str):
    with get_session() as session:
        return ButtonList(
            buttons=[
                ButtonResponse(
                    uuid=x.uuid,
                    text=x.text,
                    url=x.url,
                    color=x.color,
                )
                for x in session.query(Button).filter_by(
                    project_uuid=project_uuid
                ).order_by(
                    Button.creation_date.desc()
                ).all()
            ]
        )
