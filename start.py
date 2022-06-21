from os import environ
from os.path import exists
from os import mkdir
from os.path import join
from os.path import abspath
from os.path import dirname
from sys import argv
from uvicorn import run
from fastapi import FastAPI
from fastapi import APIRouter
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

if __name__ == "__main__":
    if not exists(".JWT_SECRET"):
        getattr(__import__("key"), "create")()

    load_dotenv()

    environ.__setitem__("STORAGE_PATH", join(dirname(abspath(__file__)), ".storage"))
    if not exists(environ['STORAGE_PATH']):
        mkdir(".storage")

    run(
        app="start:app",
        host="127.0.0.1",
        port=19564,
        log_level="info"
    )
else:
    app = FastAPI(
        title="My Portfolio API",
        description="https://github.com/chick0/mypt_api",
        version="3.0.0",
        openapi_url=None if '--no-docs' in argv else "/openapi.json"
    )

    versions = [
        "v3",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            x.strip()
            for x in environ['CORS_ORIGIN'].split(",")
        ],
        allow_methods=[
            "GET",
            "PATCH",
            "POST",
            "DELETE"
        ],
        allow_headers=[
            "Authorization"
        ]
    )

    for version in [__import__(x) for x in versions]:
        dummy = APIRouter(
            prefix="/" + version.__name__,
            tags=[version.__name__]
        )

        for router in [getattr(x, "router") for x in [getattr(version, x) for x in version.__all__]]:
            dummy.include_router(router=router)

        app.include_router(router=dummy)
