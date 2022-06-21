from pydantic import BaseModel
from v3.storage.models import Date


class LoginRequest(BaseModel):
    email: str
    password: str
    verify_method: str


class LoginResponse(BaseModel):
    user_id: int
    request_id: int


class TokenStatus(BaseModel):
    status: bool
    ttl: int


class TokenResponse(BaseModel):
    token: str


class TokenRevokeStatus(BaseModel):
    status: bool


class Session(BaseModel):
    id: int
    ip: str
    creation_date: Date
    revoked: bool
    same: bool


class SessionList(BaseModel):
    sessionList: list[Session]


class SessionRevokeStatus(BaseModel):
    status: bool


class VerifyRequest(BaseModel):
    user_id: int
    request_id: int
    token: str


class PasswordUpdateRequest(BaseModel):
    old_password: str
    new_password: str


class PasswordUpdateStatus(BaseModel):
    status: bool
