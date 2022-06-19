from datetime import datetime

from os import environ
from os.path import exists
from os.path import join

from v3.storage.models import Date


def to_date(date: datetime) -> Date:
    return Date(
        timestamp=round(date.timestamp()),
        pretty=date.strftime("%Y년 %m월 %d일 / %H시 %M분"),
    )


def get_path(uuid: str) -> str:
    path = join(
        environ['STORAGE_PATH'],
        uuid
    )

    return path


def get_safe_path(uuid: str) -> str or None:
    path = get_path(uuid=uuid)

    if exists(path=path):
        return path
    else:
        return None

