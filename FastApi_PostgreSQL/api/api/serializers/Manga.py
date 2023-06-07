from ..models.Manga import Manga
from ..serializers import Serializer

from .File import ImageSerializer


class MangaSerializer(Serializer):
    class Meta:
        orm_model = Manga

    name: str
    image_url: str = None
    status_name: str = None

    series: 'SeriesSerializer' = None
    image: ImageSerializer = None
    status: 'StatusSerializer' = None
    chapters: list['MangaChapterSerializer'] = []

    authors: list['AuthorSerializer'] = []


from .Series import SeriesSerializer
from .Author import AuthorSerializer
from .Status import StatusSerializer
from .Chapter import MangaChapterSerializer
MangaSerializer.update_forward_refs()
