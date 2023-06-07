from fastapi import APIRouter, HTTPException

from ..serializers.Chapter import NovelChapter, ReadNovelChapter, MangaChapter, ReadMangaChapter, AnimeChapter, ReadAnimeChapter
from ..tools.ModelType import SortingType

novel_chapter_router = APIRouter()


@novel_chapter_router.get("/{novel_name}/All", response_model=list[ReadNovelChapter], response_description="All Novel Chapter Retrieved")
async def get_all_novel_chapter(novel_name: str):
    filter_by = {"name": novel_name}
    if result := await NovelChapter.get_all(filter_by, [("number", int(SortingType.ascending))]):
        return result
    raise HTTPException(status_code=404, detail=f"No {NovelChapter.__name__} instances found")


@novel_chapter_router.get("/{novel_name}/{chapter_number}", response_model=ReadNovelChapter, response_description="Novel Chapter Retrieved")
async def get_novel_chapter(novel_name: str, chapter_number: int):
    filter_by = {"name": novel_name, "number": chapter_number}
    if result := await NovelChapter.get(filter_by):
        return result
    raise HTTPException(status_code=404, detail=f"{NovelChapter.__name__}: {filter_by} not found")


@novel_chapter_router.post("/{novel_name}/{chapter_number}", response_model=ReadNovelChapter, response_description="Novel Chapter Created")
async def create_novel_chapter(novel_name: str, chapter_number: int, chapter: NovelChapter):
    filter_by = {"name": novel_name, "number": chapter_number}
    if result := await chapter.create(filter_by, chapter.dict()):
        return result
    raise HTTPException(status_code=422, detail=f"{chapter.__class__.__name__}: {filter_by} already exist")


@novel_chapter_router.put("/{novel_name}/{chapter_number}", response_model=ReadNovelChapter, response_description="Novel Chapter Updated")
async def update_novel_chapter(novel_name: str, chapter_number: int, chapter: NovelChapter):
    filter_by = {"name": novel_name, "number": chapter_number}
    if result := await chapter.update(filter_by, chapter.dict()):
        return result
    raise HTTPException(status_code=422, detail=f"Failed to update {chapter.__class__.__name__}: {filter_by}")


@novel_chapter_router.delete("/{novel_name}/{chapter_number}", response_model=bool, response_description="Novel Chapter Deleted")
async def delete_novel_chapter(novel_name: str, chapter_number: int):
    filter_by = {"name": novel_name, "number": chapter_number}
    if result := await NovelChapter.delete(filter_by):
        return result
    raise HTTPException(status_code=422, detail=f"Failed to delete {NovelChapter.__name__}: {filter_by}")


manga_chapter_router = APIRouter()


@manga_chapter_router.get("/{manga_name}/All", response_model=list[ReadMangaChapter], response_description="All Manga Chapter Retrieved")
async def get_all_manga_chapter(manga_name: str):
    filter_by = {"name": manga_name}
    if result := await MangaChapter.get_all(filter_by, [("number", int(SortingType.ascending))]):
        return result
    raise HTTPException(status_code=404, detail=f"No {MangaChapter.__name__} instances found")


@manga_chapter_router.get("/{manga_name}/{chapter_number}", response_model=ReadMangaChapter, response_description="Manga Chapter Retrieved")
async def get_manga_chapter(manga_name: str, chapter_number: int):
    filter_by = {"name": manga_name, "number": chapter_number}
    if result := await MangaChapter.get(filter_by):
        return result
    raise HTTPException(status_code=404, detail=f"{MangaChapter.__name__}: {filter_by} not found")


@manga_chapter_router.post("/{manga_name}/{chapter_number}", response_model=ReadMangaChapter, response_description="Manga Chapter Created")
async def create_manga_chapter(manga_name: str, chapter_number: int, chapter: MangaChapter):
    filter_by = {"name": manga_name, "number": chapter_number}
    if result := await chapter.create(filter_by, chapter.dict()):
        return result
    raise HTTPException(status_code=422, detail=f"{chapter.__class__.__name__}: {filter_by} already exist")


@manga_chapter_router.put("/{manga_name}/{chapter_number}", response_model=ReadMangaChapter, response_description="Manga Chapter Updated")
async def update_manga_chapter(manga_name: str, chapter_number: int, chapter: MangaChapter):
    filter_by = {"name": manga_name, "number": chapter_number}
    if result := await chapter.update(filter_by, chapter.dict()):
        return result
    raise HTTPException(status_code=422, detail=f"Failed to update {chapter.__class__.__name__}: {filter_by}")


@manga_chapter_router.delete("/{manga_name}/{chapter_number}", response_model=bool, response_description="Manga Chapter Deleted")
async def delete_manga_chapter(manga_name: str, chapter_number: int):
    filter_by = {"name": manga_name, "number": chapter_number}
    if result := await MangaChapter.delete(filter_by):
        return result
    raise HTTPException(status_code=422, detail=f"Failed to delete {MangaChapter.__name__}: {filter_by}")


anime_chapter_router = APIRouter()


@anime_chapter_router.get("/{anime_name}/All", response_model=list[ReadAnimeChapter], response_description="All Anime Chapter Retrieved")
async def get_all_anime_chapter(anime_name: str):
    filter_by = {"name": anime_name}
    if result := await AnimeChapter.get_all(filter_by, [("number", int(SortingType.ascending))]):
        return result
    raise HTTPException(status_code=404, detail=f"No {AnimeChapter.__name__} instances found")


@anime_chapter_router.get("/{anime_name}/{chapter_number}", response_model=ReadAnimeChapter, response_description="Anime Chapter Retrieved")
async def get_anime_chapter(anime_name: str, chapter_number: int):
    filter_by = {"name": anime_name, "number": chapter_number}
    if result := await AnimeChapter.get(filter_by):
        return result
    raise HTTPException(status_code=404, detail=f"{AnimeChapter.__name__}: {filter_by} not found")


@anime_chapter_router.post("/{anime_name}/{chapter_number}", response_model=ReadAnimeChapter, response_description="Anime Chapter Created")
async def create_anime_chapter(anime_name: str, chapter_number: int, chapter: AnimeChapter):
    filter_by = {"name": anime_name, "number": chapter_number}
    if result := await chapter.create(filter_by, chapter.dict()):
        return result
    raise HTTPException(status_code=422, detail=f"{chapter.__class__.__name__}: {filter_by} already exist")


@anime_chapter_router.put("/{anime_name}/{chapter_number}", response_model=ReadAnimeChapter, response_description="Anime Chapter Updated")
async def update_anime_chapter(anime_name: str, chapter_number: int, chapter: AnimeChapter):
    filter_by = {"name": anime_name, "number": chapter_number}
    if result := await chapter.update(filter_by, chapter.dict()):
        return result
    raise HTTPException(status_code=422, detail=f"Failed to update {chapter.__class__.__name__}: {filter_by}")


@anime_chapter_router.delete("/{anime_name}/{chapter_number}", response_model=bool, response_description="Anime Chapter Deleted")
async def delete_anime_chapter(anime_name: str, chapter_number: int):
    filter_by = {"name": anime_name, "number": chapter_number}
    if result := await AnimeChapter.delete(filter_by):
        return result
    raise HTTPException(status_code=422, detail=f"Failed to delete {AnimeChapter.__name__}: {filter_by}")
