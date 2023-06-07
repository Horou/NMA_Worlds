from fastapi import APIRouter

from ..serializers.Author import AuthorSerializer


author_router = APIRouter()


@author_router.get("/", response_model=list[AuthorSerializer])
async def get_all():
    return await AuthorSerializer.get_all({})


@author_router.get("/{name}", response_model=AuthorSerializer)
async def get(name: str):
    return await AuthorSerializer.get({"name": name})


@author_router.post("/", response_model=AuthorSerializer)
async def create(user: AuthorSerializer):
    return await user.create()


@author_router.put("/{name}", response_model=AuthorSerializer)
async def update(name: str, user: AuthorSerializer):
    return await user.update({"name": name})


@author_router.post("/multi", response_model=list[AuthorSerializer])
async def merge(data: list[AuthorSerializer]):
    return await AuthorSerializer.merge(data)


@author_router.delete("/{name}", response_model=bool)
async def delete(name: str):
    return await AuthorSerializer.delete({"name": name})
