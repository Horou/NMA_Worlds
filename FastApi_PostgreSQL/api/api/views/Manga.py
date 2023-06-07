from fastapi import APIRouter

from ..serializers.Manga import MangaSerializer


manga_router = APIRouter()


@manga_router.get("/", response_model=list[MangaSerializer])
async def get_all():
    return await MangaSerializer.get_all({})


@manga_router.get("/{name}", response_model=MangaSerializer)
async def get(name: str):
    return await MangaSerializer.get({"name": name})


@manga_router.post("/", response_model=MangaSerializer)
async def create(user: MangaSerializer):
    return await user.create()


@manga_router.put("/{name}", response_model=MangaSerializer)
async def update(name: str, user: MangaSerializer):
    return await user.update({"name": name})


@manga_router.post("/multi", response_model=list[MangaSerializer])
async def merge(data: list[MangaSerializer]):
    return await MangaSerializer.merge(data)


@manga_router.delete("/{name}", response_model=bool)
async def delete(name: str):
    return await MangaSerializer.delete({"name": name})
