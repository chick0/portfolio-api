__all__ = [
    "history",
    "login",
    "logout",
]

from . import *
from fastapi import APIRouter

router = APIRouter(
    prefix="/auth",
    tags=['auth']
)

for e in __all__:
    router.include_router(getattr(locals()[e], "router"))
