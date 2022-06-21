__all__ = [
    "delete",
    "detail",
    "edit",
]

from . import *
from fastapi import APIRouter

router = APIRouter(prefix="/project")

for e in __all__:
    router.include_router(getattr(locals()[e], "router"))
