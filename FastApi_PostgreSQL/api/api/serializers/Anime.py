from ..models.Anime import Anime
from ..serializers import Serializer

from .File import ImageSerializer


class AnimeSerializer(Serializer):
    class Meta:
        orm_model = Anime

    name: str
    image_url: str = None
    status_name: str = None

    series: 'SeriesSerializer' = None
    image: ImageSerializer = None
    status: 'StatusSerializer' = None
    chapters: list['AnimeChapterSerializer'] = []

    authors: list['AuthorSerializer'] = []


from .Series import SeriesSerializer
from .Author import AuthorSerializer
from .Status import StatusSerializer
from .Chapter import AnimeChapterSerializer
AnimeSerializer.update_forward_refs()
