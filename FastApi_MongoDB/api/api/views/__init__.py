from fastapi import APIRouter
from .Chapter import novel_chapter_router, manga_chapter_router, anime_chapter_router
from .Series import series_router, novel_router, manga_router, anime_router
from .Other import genre_router, tag_router, status_router, author_router

api_router = APIRouter()
api_router.include_router(series_router, prefix="/Series", tags=["Series"])
api_router.include_router(novel_router, prefix="/Novel", tags=["Novel"])
api_router.include_router(manga_router, prefix="/Manga", tags=["Manga"])
api_router.include_router(anime_router, prefix="/Anime", tags=["Anime"])
api_router.include_router(novel_chapter_router, prefix="/Novel", tags=["Novel_Chapter"])
api_router.include_router(manga_chapter_router, prefix="/Manga", tags=["Manga_Chapter"])
api_router.include_router(anime_chapter_router, prefix="/Anime", tags=["Anime_Chapter"])
api_router.include_router(genre_router, prefix="/Genre", tags=["Genre"])
api_router.include_router(tag_router, prefix="/Tag", tags=["Tag"])
api_router.include_router(status_router, prefix="/Status", tags=["Status"])
api_router.include_router(author_router, prefix="/Author", tags=["Author"])
