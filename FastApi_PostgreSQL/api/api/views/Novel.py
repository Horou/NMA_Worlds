from fastapi import APIRouter

from ..serializers.Novel import NovelSerializer


novel_router = APIRouter()


@novel_router.get("/", response_model=list[NovelSerializer])
async def get_all():
    return await NovelSerializer.get_all({})


@novel_router.get("/{name}", response_model=NovelSerializer)
async def get(name: str):
    return await NovelSerializer.get({"name": name})


@novel_router.post("/", response_model=NovelSerializer)
async def create(user: NovelSerializer):
    return await user.create()


@novel_router.put("/{name}", response_model=NovelSerializer)
async def update(name: str, user: NovelSerializer):
    return await user.update({"name": name})


@novel_router.post("/multi", response_model=list[NovelSerializer])
async def merge(data: list[NovelSerializer]):
    return await NovelSerializer.merge(data)


@novel_router.delete("/{name}", response_model=bool)
async def delete(name: str):
    return await NovelSerializer.delete({"name": name})
