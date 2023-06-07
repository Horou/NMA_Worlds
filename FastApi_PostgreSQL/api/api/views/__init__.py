from fastapi import APIRouter

from .Series import series_router
from .Novel import novel_router
from .Manga import manga_router
from .Anime import anime_router
from .Chapter import novel_chapter_router, manga_chapter_router, anime_chapter_router
from .Tag import tag_router, genre_router
from .Status import status_router
from .Author import author_router

api_router = APIRouter()
api_router.include_router(series_router, prefix="/series", tags=["series"])
api_router.include_router(novel_router, prefix="/novel", tags=["novel"])
api_router.include_router(manga_router, prefix="/manga", tags=["manga"])
api_router.include_router(anime_router, prefix="/anime", tags=["anime"])
api_router.include_router(novel_chapter_router, prefix="/novel_chapter", tags=["novel_chapter"])
api_router.include_router(manga_chapter_router, prefix="/manga_chapter", tags=["manga_chapter"])
api_router.include_router(anime_chapter_router, prefix="/anime_chapter", tags=["anime_chapter"])
api_router.include_router(tag_router, prefix="/tag", tags=["tag"])
api_router.include_router(genre_router, prefix="/genre", tags=["genre"])
api_router.include_router(status_router, prefix="/status", tags=["status"])
api_router.include_router(author_router, prefix="/author", tags=["author"])
