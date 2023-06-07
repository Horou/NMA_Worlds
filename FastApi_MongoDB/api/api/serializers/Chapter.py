from datetime import datetime

from ..models.Chapter import NovelChapter, MangaChapter, AnimeChapter


class ReadNovelChapter(NovelChapter):
    created_at: datetime
    updated_at: datetime


class ReadMangaChapter(MangaChapter):
    created_at: datetime
    updated_at: datetime


class ReadAnimeChapter(AnimeChapter):
    created_at: datetime
    updated_at: datetime
