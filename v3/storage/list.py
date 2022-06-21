from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import HTTPBearer

from sql import get_session
from sql.models import Storage
from utils.token import parse_token
from v3.utils import to_date
from v3.storage.models import StorageItem
from v3.storage.models import StorageItems

router = APIRouter()
auth_scheme = HTTPBearer()


@router.get(
    "/list",
    description="업로드된 파일들의 목록을 불러옵니다.",
    response_model=StorageItems
)
async def storage_item_list(token=Depends(auth_scheme)):
    parse_token(token=token)
    session = get_session()

    return StorageItems(
        items=[
            StorageItem(
                uuid=x.uuid,
                name=x.name,
                creation_date=to_date(date=x.creation_date)
            ) for x in session.query(Storage).order_by(
                Storage.creation_date.desc()
            ).with_entities(
                Storage.uuid,
                Storage.name,
                Storage.creation_date,
            ).all()
        ]
    )
