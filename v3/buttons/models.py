from pydantic import BaseModel


class ButtonRequest(BaseModel):
    text: str
    url: str
    color: str


class ButtonResponse(BaseModel):
    uuid: str
    text: str
    url: str
    color: str


class ButtonList(BaseModel):
    buttons: list[ButtonResponse]


class ButtonDeleteStatus(BaseModel):
    status: bool


class ButtonEditStatus(BaseModel):
    status: bool
