__all__ = [
    "create",
    "delete",
    "edit",
    "get",
]

from . import *
from fastapi import APIRouter

router = APIRouter(prefix="/button")

for e in __all__:
    router.include_router(getattr(locals()[e], "router"))
