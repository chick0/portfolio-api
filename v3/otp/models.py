from pydantic import BaseModel


class OTPResult(BaseModel):
    url: str


class OTPDeleteStatus(BaseModel):
    status: bool
