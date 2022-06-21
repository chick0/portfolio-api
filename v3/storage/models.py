from pydantic import BaseModel


class Date(BaseModel):
    timestamp: int
    pretty: str
    ymd: str


class StorageItem(BaseModel):
    uuid: str
    name: str
    creation_date: Date


class StorageItems(BaseModel):
    items: list[StorageItem]


class StorageDelete(BaseModel):
    result: bool  # true=success
