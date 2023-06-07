from fastapi import APIRouter, HTTPException

from ..tools.ModelType import SortingType
from ..serializers.Other import Genre, ReadGenre, Tag, ReadTag, Status, ReadStatus, Author, ReadAuthor
from ..tools.ModelType import StatusType

genre_router = APIRouter()


@genre_router.get("/All", response_model=list[ReadGenre], response_description="All Genre Retrieved")
async def get_all_genre():
    if result := await Genre.get_all({}, [("name", int(SortingType.ascending))]):
        return result
    raise HTTPException(status_code=404, detail=f"No {Genre.__name__} instances found")


@genre_router.get("/{genre_name}", response_model=ReadGenre, response_description="Genre Retrieved")
async def get_genre(genre_name: str):
    filter_by = {"name": genre_name}
    if result := await Genre.get(filter_by):
        return result
    raise HTTPException(status_code=404, detail=f"{Genre.__name__}: {filter_by} not found")


@genre_router.post("/{genre_name}", response_model=ReadGenre, response_description="Genre Created")
async def create_genre(genre_name: str, genre: Genre):
    filter_by = {"name": genre_name}
    if result := await genre.create(filter_by, genre.dict()):
        return result
    raise HTTPException(status_code=422, detail=f"{genre.__class__.__name__}: {filter_by} already exist")


@genre_router.put("/{genre_name}", response_model=ReadGenre, response_description="Genre Updated")
async def update_genre(genre_name: str, genre: Genre):
    filter_by = {"name": genre_name}
    if result := await genre.update(filter_by, genre.dict()):
        return result
    raise HTTPException(status_code=422, detail=f"Failed to update {genre.__class__.__name__}: {filter_by}")


@genre_router.delete("/{genre_name}", response_model=bool, response_description="Genre Deleted")
async def delete_genre(genre_name: str):
    filter_by = {"name": genre_name}
    if result := await Genre.delete(filter_by):
        return result
    raise HTTPException(status_code=422, detail=f"Failed to delete {Genre.__name__}: {filter_by}")


tag_router = APIRouter()


@tag_router.get("/All", response_model=list[ReadTag], response_description="All Tag Retrieved")
async def get_all_tag():
    if result := await Tag.get_all({}, [("name", int(SortingType.ascending))]):
        return result
    raise HTTPException(status_code=404, detail=f"No {Tag.__name__} instances found")


@tag_router.get("/{tag_name}", response_model=ReadTag, response_description="Tag Retrieved")
async def get_tag(tag_name: str):
    filter_by = {"name": tag_name}
    if result := await Tag.get(filter_by):
        return result
    raise HTTPException(status_code=404, detail=f"{Tag.__name__}: {filter_by} not found")


@tag_router.post("/{tag_name}", response_model=ReadTag, response_description="Tag Created")
async def create_tag(tag_name: str, tag: Tag):
    filter_by = {"name": tag_name}
    if result := await tag.create(filter_by, tag.dict()):
        return result
    raise HTTPException(status_code=422, detail=f"{tag.__class__.__name__}: {filter_by} already exist")


@tag_router.put("/{tag_name}", response_model=ReadTag, response_description="Tag Updated")
async def update_tag(tag_name: str, tag: Tag):
    filter_by = {"name": tag_name}
    if result := await tag.update(filter_by, tag.dict()):
        return result
    raise HTTPException(status_code=422, detail=f"Failed to update {tag.__class__.__name__}: {filter_by}")


@tag_router.delete("/{tag_name}", response_model=bool, response_description="Tag Deleted")
async def delete_tag(tag_name: str):
    filter_by = {"name": tag_name}
    if result := await Tag.delete(filter_by):
        return result
    raise HTTPException(status_code=422, detail=f"Failed to delete {Tag.__name__}: {filter_by}")


status_router = APIRouter()


@status_router.get("/All", response_model=list[ReadStatus], response_description="All Status Retrieved")
async def get_all_status():
    if result := await Status.get_all({}, [("name", int(SortingType.ascending))]):
        return result
    raise HTTPException(status_code=404, detail=f"No {Status.__name__} instances found")


@status_router.get("/{status_name}", response_model=ReadStatus, response_description="Status Retrieved")
async def get_status(status_name: StatusType):
    filter_by = {"name": status_name}
    if result := await Status.get(filter_by):
        return result
    raise HTTPException(status_code=404, detail=f"{Status.__name__}: {filter_by} not found")


@status_router.post("/{status_name}", response_model=ReadStatus, response_description="Status Created")
async def create_status(status_name: StatusType, status: Status):
    filter_by = {"name": status_name}
    if result := await status.create(filter_by, status.dict()):
        return result
    raise HTTPException(status_code=422, detail=f"{status.__class__.__name__}: {filter_by} already exist")


@status_router.put("/{status_name}", response_model=ReadStatus, response_description="Status Updated")
async def update_status(status_name: StatusType, status: Status):
    filter_by = {"name": status_name}
    if result := await status.update(filter_by, status.dict()):
        return result
    raise HTTPException(status_code=422, detail=f"Failed to update {status.__class__.__name__}: {filter_by}")


@status_router.delete("/{status_name}", response_model=bool, response_description="Status Deleted")
async def delete_status(status_name: StatusType):
    filter_by = {"name": status_name}
    if result := await Status.delete(filter_by):
        return result
    raise HTTPException(status_code=422, detail=f"Failed to delete {Status.__name__}: {filter_by}")


author_router = APIRouter()


@author_router.get("/All", response_model=list[ReadAuthor], response_description="All Author Retrieved")
async def get_all_author():
    if result := await Author.get_all({}, [("name", int(SortingType.ascending))]):
        return result
    raise HTTPException(status_code=404, detail=f"No {Author.__name__} instances found")


@author_router.get("/{author_name}", response_model=ReadAuthor, response_description="Author Retrieved")
async def get_author(author_name: str):
    filter_by = {"name": author_name}
    if result := await Author.get(filter_by):
        return result
    raise HTTPException(status_code=404, detail=f"{Author.__name__}: {filter_by} not found")


@author_router.post("/{author_name}", response_model=ReadAuthor, response_description="Author Created")
async def create_author(author_name: str, author: Author):
    filter_by = {"name": author_name}
    if result := await author.create(filter_by, author.dict()):
        return result
    raise HTTPException(status_code=422, detail=f"{author.__class__.__name__}: {filter_by} already exist")


@author_router.put("/{author_name}", response_model=ReadAuthor, response_description="Author Updated")
async def update_author(author_name: str, author: Author):
    filter_by = {"name": author_name}
    if result := await author.update(filter_by, author.dict()):
        return result
    raise HTTPException(status_code=422, detail=f"Failed to update {author.__class__.__name__}: {filter_by}")


@author_router.delete("/{author_name}", response_model=bool, response_description="Author Deleted")
async def delete_author(author_name: str):
    filter_by = {"name": author_name}
    if result := await Author.delete(filter_by):
        return result
    raise HTTPException(status_code=422, detail=f"Failed to delete {Author.__name__}: {filter_by}")
