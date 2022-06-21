from os import remove
from datetime import datetime

from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import HTTPBearer

from sql import get_session
from sql.models import Storage
from utils.token import parse_token
from v3.utils import to_date
from v3.utils import get_path
from v3.storage.models import StorageItem
from v3.storage.models import StorageDelete

router = APIRouter(prefix="/manage")
auth_scheme = HTTPBearer()


@router.post(
    "/{uuid}",
    description="업로드된 파일을 수정합니다.",
    response_model=StorageItem
)
async def storage_edit(uuid: str, file: UploadFile, token=Depends(auth_scheme)):
    parse_token(token=token)

    creation_date = datetime.now()
    stream = await file.read()

    session = get_session()
    storage: Storage = session.query(Storage).filter_by(
        uuid=uuid
    ).first()

    storage.name = file.filename
    storage.creation_date = creation_date
    session.commit()
    session.close()

    with open(get_path(uuid=uuid), mode="wb") as writer:
        writer.write(stream)

    return StorageItem(
        uuid=uuid,
        name=file.filename,
        creation_date=to_date(creation_date)
    )


@router.delete(
    "/{uuid}",
    description="업로드된 파일을 삭제합니다.",
    response_model=StorageDelete
)
async def storage_delete(uuid: str, token=Depends(auth_scheme)):
    parse_token(token=token)

    session = get_session()

    deleted = session.query(Storage).filter_by(
        uuid=uuid
    ).delete()

    if deleted == 1:
        session.commit()

        try:
            remove(get_path(uuid=uuid))
        except (FileNotFoundError, Exception):
            raise HTTPException(
                status_code=400,
                detail={
                    "alert": "파일 삭제에 실패했습니다. 서버에서 수동으로 삭제해주세요."
                }
            )

    session.close()

    return StorageDelete(
        result=deleted == 1
    )
