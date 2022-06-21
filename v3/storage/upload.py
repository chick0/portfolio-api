from uuid import uuid4

from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import Depends
from fastapi import status as _
from fastapi.security import HTTPBearer

from sql import get_session
from sql.models import Storage
from utils.token import parse_token
from v3.utils import get_path
from v3.utils import to_date
from v3.storage.models import StorageItem

router = APIRouter()
auth_scheme = HTTPBearer()
HTTP_201_CREATED = _.HTTP_201_CREATED


@router.post(
    '/upload',
    description="파일을 업로드 합니다.",
    response_model=StorageItem,
    status_code=HTTP_201_CREATED
)
async def storage_upload(file: UploadFile, token=Depends(auth_scheme)):
    parse_token(token=token)

    session = get_session()
    stream = await file.read()

    uuid = uuid4().__str__()

    storage = Storage()
    storage.uuid = uuid
    storage.name = file.filename
    storage.size = len(stream)

    session.add(storage)
    session.commit()

    date = to_date(date=storage.creation_date)
    session.close()

    with open(get_path(uuid=uuid), mode="wb") as writer:
        writer.write(stream)

    return StorageItem(
        uuid=uuid,
        name=file.filename,
        creation_date=date
    )
