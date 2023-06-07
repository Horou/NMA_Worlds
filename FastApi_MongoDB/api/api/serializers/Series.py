from datetime import datetime

from pydantic import Field

from ..models.Series import Novel, Manga, Anime, Series
from .Chapter import ReadNovelChapter, ReadMangaChapter, ReadAnimeChapter


class ReadNovel(Novel):
    chapters: list[ReadNovelChapter] = Field(default=[])
    created_at: datetime
    updated_at: datetime


class ReadManga(Manga):
    chapters: list[ReadMangaChapter] = Field(default=[])
    created_at: datetime
    updated_at: datetime


class ReadAnime(Anime):
    episodes: list[ReadAnimeChapter] = Field(default=[])
    created_at: datetime
    updated_at: datetime


class ReadSeries(Series):
    novel: ReadNovel = Field(default=None)
    manga: ReadManga = Field(default=None)
    anime: ReadAnime = Field(default=None)
    created_at: datetime
    updated_at: datetime
