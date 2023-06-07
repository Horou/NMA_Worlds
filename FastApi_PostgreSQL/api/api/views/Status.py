from fastapi import APIRouter

from ..serializers.Status import StatusSerializer


status_router = APIRouter()


@status_router.get("/", response_model=list[StatusSerializer])
async def get_all():
    return await StatusSerializer.get_all({})


@status_router.get("/{name}", response_model=StatusSerializer)
async def get(name: str):
    return await StatusSerializer.get({"name": name})


@status_router.post("/", response_model=StatusSerializer)
async def create(user: StatusSerializer):
    return await user.create()


@status_router.put("/{name}", response_model=StatusSerializer)
async def update(name: str, user: StatusSerializer):
    return await user.update({"name": name})


@status_router.post("/multi", response_model=list[StatusSerializer])
async def merge(data: list[StatusSerializer]):
    return await StatusSerializer.merge(data)


@status_router.delete("/{name}", response_model=bool)
async def delete(name: str):
    return await StatusSerializer.delete({"name": name})
