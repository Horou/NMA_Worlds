from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .views import api_router
from .config import settings


def init_app():
    _app = FastAPI(
        root_path=settings.ROOT_PATH,
        title="NMA Worlds",
        description="Worlds of Novel, Manga and Anime",
        version="1",
    )
    _app.mount(settings.FILES_PATH, StaticFiles(directory=settings.FILES_PATH), name="media")
    _app.include_router(api_router)
    return _app


app = init_app()


@app.get("/", tags=["Root"])
async def read_root():
    return {"NMA Worlds": "Worlds of Novel, Manga and Anime"}

