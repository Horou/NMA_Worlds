from fastapi import APIRouter

from ..serializers.Series import SeriesSerializer


series_router = APIRouter()


@series_router.get("/", response_model=list[SeriesSerializer])
async def get_all():
    return await SeriesSerializer.get_all({})


@series_router.get("/{name}", response_model=SeriesSerializer)
async def get(name: str):
    return await SeriesSerializer.get({"name": name})


@series_router.post("/", response_model=SeriesSerializer)
async def create(user: SeriesSerializer):
    return await user.create()


@series_router.put("/{name}", response_model=SeriesSerializer)
async def update(name: str, user: SeriesSerializer):
    return await user.update({"name": name})


@series_router.post("/multi", response_model=list[SeriesSerializer])
async def merge(data: list[SeriesSerializer]):
    return await SeriesSerializer.merge(data)


@series_router.delete("/{name}", response_model=bool)
async def delete(name: str):
    return await SeriesSerializer.delete({"name": name})
