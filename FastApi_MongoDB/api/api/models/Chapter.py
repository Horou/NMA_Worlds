from pydantic import HttpUrl, Field

from ..models import Model, db
from ..tools.ModelType import NovelChapterType, MangaChapterType, AnimeChapterType


class NovelChapter(Model):
    _collection = db["NovelChapter"]
    _primary_keys = ['name', 'number']
    _parents = {}

    type: NovelChapterType = Field(default=NovelChapterType.webnovel)
    number: int = Field(default=0)
    season: int = Field(default=1)
    images: list[HttpUrl] | None = Field(default=[])
    manga_chapter: HttpUrl | None = Field(default=None)
    anime_episode: HttpUrl | None = Field(default=None)
    source: HttpUrl | None = Field(default=None)


class MangaChapter(Model):
    _collection = db["MangaChapter"]
    _primary_keys = ['name', 'number']
    _parents = {}

    type: MangaChapterType = Field(default=MangaChapterType.manga)
    series: str = Field(default="0")
    number: int = Field(default=0)
    book: int = Field(default=1)
    images: list[HttpUrl] | None = Field(default=[])
    novel_chapter: HttpUrl | None = Field(default=None)
    anime_episode: HttpUrl | None = Field(default=None)
    source: HttpUrl | None = Field(default=None)


class AnimeChapter(Model):
    _collection = db["AnimeChapter"]
    _primary_keys = ['name', 'number']
    _parents = {}

    type: AnimeChapterType = Field(default=AnimeChapterType.episode)
    number: int = Field(default=0)
    season: int = Field(default=1)
    videos: list[HttpUrl] = Field(default=[])
    novel_chapter: HttpUrl | None = Field(default=None)
    manga_chapter: HttpUrl | None = Field(default=None)
    source: HttpUrl | None = Field(default=None)


NovelChapter.create_index()
MangaChapter.create_index()
AnimeChapter.create_index()
