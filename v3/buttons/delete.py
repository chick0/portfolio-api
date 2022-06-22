from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import HTTPBearer

from sql import get_session
from sql.models import Button
from utils.token import parse_token
from v3.buttons.models import ButtonDeleteStatus

router = APIRouter()
auth_scheme = HTTPBearer()


@router.delete(
    "/{button_uuid}",
    description="등록된 버튼을 삭제합니다.",
    response_model=ButtonDeleteStatus
)
async def delete_button(button_uuid: str, token=Depends(auth_scheme)):
    parse_token(token=token)
    session = get_session()

    deleted: Button = session.query(Button).filter_by(
        uuid=button_uuid
    ).delete()

    session.commit()
    session.close()

    return ButtonDeleteStatus(
        status=deleted == 1
    )
