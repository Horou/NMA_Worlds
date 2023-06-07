from fastapi import APIRouter

from ..serializers.Tag import TagSerializer, GenreSerializer


tag_router = APIRouter()


@tag_router.get("/", response_model=list[TagSerializer])
async def get_all():
    return await TagSerializer.get_all({})


@tag_router.get("/{name}", response_model=TagSerializer)
async def get(name: str):
    return await TagSerializer.get({"name": name})


@tag_router.post("/", response_model=TagSerializer)
async def create(user: TagSerializer):
    return await user.create()


@tag_router.put("/{name}", response_model=TagSerializer)
async def update(name: str, user: TagSerializer):
    return await user.update({"name": name})


@tag_router.post("/multi", response_model=list[TagSerializer])
async def merge(data: list[TagSerializer]):
    return await TagSerializer.merge(data)


@tag_router.delete("/{name}", response_model=bool)
async def delete(name: str):
    return await TagSerializer.delete({"name": name})


genre_router = APIRouter()


@genre_router.post("/multi", response_model=list[GenreSerializer])
async def merge(data: list[GenreSerializer]):
    return await GenreSerializer.merge(data)


@genre_router.post("/", response_model=GenreSerializer)
async def create(user: GenreSerializer):
    return await user.create()


@genre_router.get("/{name}", response_model=GenreSerializer)
async def get(name: str):
    return await GenreSerializer.get({"name": name})


@genre_router.get("/", response_model=list[GenreSerializer])
async def get_all():
    return await GenreSerializer.get_all({})


@genre_router.put("/{name}", response_model=GenreSerializer)
async def update(name: str, user: GenreSerializer):
    return await user.update({"name": name})


@genre_router.delete("/{name}", response_model=bool)
async def delete(name: str):
    return await GenreSerializer.delete({"name": name})
