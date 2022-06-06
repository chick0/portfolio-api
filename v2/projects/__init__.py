__all__ = [
    "create",
    "detail",
    "index",
]

from . import *
from fastapi import APIRouter

router = APIRouter(
    prefix="/projects",
)

for e in __all__:
    router.include_router(getattr(locals()[e], "router"))
