from fastapi import APIRouter
from fastapi import HTTPException
from fastapi.responses import FileResponse

from sql import get_session
from sql.models import Storage
from v3.utils import get_safe_path

router = APIRouter(prefix="/download")


@router.get(
    "/{uuid}",
    description="업로드된 파일을 다운받습니다.",
    response_class=FileResponse
)
async def storage_download(uuid: str):
    path = get_safe_path(uuid=uuid)
    if path is None:
        raise HTTPException(
            status_code=404,
            detail="fail to search in storage"
        )

    session = get_session()
    storage: Storage = session.query(Storage).filter_by(
        uuid=uuid
    ).first()

    if storage is None:
        raise HTTPException(
            status_code=404,
            detail="fail to search item in database"
        )

    session.close()

    return FileResponse(
        path=path,
        filename=storage.name,
        media_type="application/octet-stream"
    )
