from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import HTTPBearer

from sql import get_session
from sql.models import Button
from utils.token import parse_token
from v3.buttons.models import ButtonRequest
from v3.buttons.models import ButtonEditStatus

router = APIRouter()
auth_scheme = HTTPBearer()


@router.patch(
    "/{button_uuid}",
    description="등록된 버튼을 수정합니다.",
    response_model=ButtonEditStatus
)
async def update_button(button_uuid: str, request: ButtonRequest, token=Depends(auth_scheme)):
    parse_token(token=token)
    session = get_session()

    button: Button = session.query(Button).filter_by(
        uuid=button_uuid
    ).first()

    if button is None:
        raise HTTPException(
            status_code=400,
            detail={
                "alert": "등록된 버튼이 아닙니다."
            }
        )

    button.text = request.text.strip()
    button.url = request.url.strip()
    button.color = request.color.strip()

    session.commit()
    session.close()

    return ButtonEditStatus(
        result=True,
    )
