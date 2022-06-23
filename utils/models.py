from pydantic import BaseModel


class TokenPayload(BaseModel):
    user_id: int
    session_id: int
    exp: int
