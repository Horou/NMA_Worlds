from fastapi import APIRouter

from ..serializers.Anime import AnimeSerializer


anime_router = APIRouter()


@anime_router.get("/", response_model=list[AnimeSerializer])
async def get_all():
    return await AnimeSerializer.get_all({})


@anime_router.get("/{name}", response_model=AnimeSerializer)
async def get(name: str):
    return await AnimeSerializer.get({"name": name})


@anime_router.post("/", response_model=AnimeSerializer)
async def create(user: AnimeSerializer):
    return await user.create()


@anime_router.put("/{name}", response_model=AnimeSerializer)
async def update(name: str, user: AnimeSerializer):
    return await user.update({"name": name})


@anime_router.post("/multi", response_model=list[AnimeSerializer])
async def merge(data: list[AnimeSerializer]):
    return await AnimeSerializer.merge(data)


@anime_router.delete("/{name}", response_model=bool)
async def delete(name: str):
    return await AnimeSerializer.delete({"name": name})
