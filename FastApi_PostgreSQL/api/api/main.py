from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .views import api_router
from .config import settings
from .database import db


def init_app():
    _app = FastAPI(
        root_path=settings.ROOT_PATH,
        title="NMA Worlds",
        description="Worlds of Novel, Manga and Anime",
        version="1",
    )
    _app.mount(settings.FILES_PATH, StaticFiles(directory=settings.FILES_PATH), name="media")
    _app.include_router(api_router)

    db.init()

    @_app.on_event("startup")
    async def startup():
        await db.create_all()

    @_app.on_event("shutdown")
    async def shutdown():
        await db.close()

    return _app


app = init_app()


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}

