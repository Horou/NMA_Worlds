from fastapi import APIRouter

from ..serializers.Chapter import NovelChapterSerializer, MangaChapterSerializer, AnimeChapterSerializer


novel_chapter_router = APIRouter()


@novel_chapter_router.get("/", response_model=list[NovelChapterSerializer])
async def get_all():
    return await NovelChapterSerializer.get_all({})


@novel_chapter_router.get("/{name}", response_model=NovelChapterSerializer)
async def get(name: str):
    return await NovelChapterSerializer.get({"name": name})


@novel_chapter_router.post("/", response_model=NovelChapterSerializer)
async def create(user: NovelChapterSerializer):
    return await user.create()


@novel_chapter_router.put("/{name}", response_model=NovelChapterSerializer)
async def update(name: str, user: NovelChapterSerializer):
    return await user.update({"name": name})


@novel_chapter_router.post("/multi", response_model=list[NovelChapterSerializer])
async def merge(data: list[NovelChapterSerializer]):
    return await NovelChapterSerializer.merge(data)


@novel_chapter_router.delete("/{name}", response_model=bool)
async def delete(name: str):
    return await NovelChapterSerializer.delete({"name": name})


manga_chapter_router = APIRouter()


@manga_chapter_router.get("/", response_model=list[MangaChapterSerializer])
async def get_all():
    return await MangaChapterSerializer.get_all({})


@manga_chapter_router.get("/{name}", response_model=MangaChapterSerializer)
async def get(name: str):
    return await MangaChapterSerializer.get({"name": name})


@manga_chapter_router.post("/", response_model=MangaChapterSerializer)
async def create(user: MangaChapterSerializer):
    return await user.create()


@manga_chapter_router.put("/{name}", response_model=MangaChapterSerializer)
async def update(name: str, user: MangaChapterSerializer):
    return await user.update({"name": name})


@manga_chapter_router.post("/multi", response_model=list[MangaChapterSerializer])
async def merge(data: list[MangaChapterSerializer]):
    return await MangaChapterSerializer.merge(data)


@manga_chapter_router.delete("/{name}", response_model=bool)
async def delete(name: str):
    return await MangaChapterSerializer.delete({"name": name})


anime_chapter_router = APIRouter()


@anime_chapter_router.get("/", response_model=list[AnimeChapterSerializer])
async def get_all():
    return await AnimeChapterSerializer.get_all({})


@anime_chapter_router.get("/{name}", response_model=AnimeChapterSerializer)
async def get(name: str):
    return await AnimeChapterSerializer.get({"name": name})


@anime_chapter_router.post("/", response_model=AnimeChapterSerializer)
async def create(user: AnimeChapterSerializer):
    return await user.create()


@anime_chapter_router.put("/{name}", response_model=AnimeChapterSerializer)
async def update(name: str, user: AnimeChapterSerializer):
    return await user.update({"name": name})


@anime_chapter_router.post("/multi", response_model=list[AnimeChapterSerializer])
async def merge(data: list[AnimeChapterSerializer]):
    return await AnimeChapterSerializer.merge(data)


@anime_chapter_router.delete("/{name}", response_model=bool)
async def delete(name: str):
    return await AnimeChapterSerializer.delete({"name": name})
