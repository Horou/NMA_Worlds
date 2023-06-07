from datetime import datetime

from ..models.Chapter import NovelChapter, MangaChapter, AnimeChapter
from ..serializers import Serializer

from .File import AnimeVideoSerializer, MangaPageSerializer


class NovelChapterSerializer(Serializer):
    class Meta:
        orm_model = NovelChapter

    number: float
    novel_name: str
    season: int = None
    name: str = None
    release_date: datetime = None

    content: str = None
    novel: 'NovelSerializer' = None


class MangaChapterSerializer(Serializer):
    class Meta:
        orm_model = MangaChapter

    number: float
    manga_name: str
    season: int = None
    name: str = None
    release_date: datetime = None

    content: list[MangaPageSerializer] = []
    manga: 'MangaSerializer' = None


class AnimeChapterSerializer(Serializer):
    class Meta:
        orm_model = AnimeChapter

    number: float
    manga_name: str
    season: int = None
    name: str = None
    release_date: datetime = None

    content: list[AnimeVideoSerializer] = []
    anime: 'AnimeSerializer' = None


from .Novel import NovelSerializer
from .Manga import MangaSerializer
from .Anime import AnimeSerializer
NovelChapterSerializer.update_forward_refs()
MangaChapterSerializer.update_forward_refs()
AnimeChapterSerializer.update_forward_refs()
