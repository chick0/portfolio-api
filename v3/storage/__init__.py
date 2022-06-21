__all__ = [
    "download",
    "list",
    "manage",
    "upload",
]

from . import *
from fastapi import APIRouter

router = APIRouter(prefix="/storage")

for e in __all__:
    router.include_router(getattr(locals()[e], "router"))
