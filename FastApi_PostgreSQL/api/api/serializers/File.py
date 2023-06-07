from pydantic import FileUrl

from ..models.File import Image, MangaPage, AnimeVideo
from ..serializers import Serializer


class ImageSerializer(Serializer):
    class Meta:
        orm_model = Image

    url: FileUrl | str = "file/to/path"


class MangaPageSerializer(Serializer):
    class Meta:
        orm_model = MangaPage

    number: int
    anime_name: str
    chapter_number: float

    url: FileUrl = None


class AnimeVideoSerializer(Serializer):
    class Meta:
        orm_model = AnimeVideo

    number: int
    anime_name: str
    chapter_number: float

    url: FileUrl = None
