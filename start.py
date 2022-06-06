from os.path import exists
from uvicorn import run
from fastapi import FastAPI
from fastapi import APIRouter
from dotenv import load_dotenv

if __name__ == "__main__":
    if not exists(".JWT_SECRET"):
        getattr(__import__("key"), "create")()

    load_dotenv()
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
        version="2.0.0"
    )

    versions = [
        "v2",
    ]

    for version in [__import__(x) for x in versions]:
        dummy = APIRouter(
            prefix="/" + version.__name__,
            tags=[version.__name__]
        )

        for router in [getattr(x, "router") for x in [getattr(version, x) for x in version.__all__]]:
            dummy.include_router(router=router)

        app.include_router(router=dummy)
