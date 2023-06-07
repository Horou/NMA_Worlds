from ..models.Novel import Novel
from ..serializers import Serializer

from .File import ImageSerializer


class NovelSerializer(Serializer):
    class Meta:
        orm_model = Novel

    name: str
    image_url: str = None
    status_name: str = None

    series: 'SeriesSerializer' = None
    image: ImageSerializer = None
    status: 'StatusSerializer' = None
    chapters: list['NovelChapterSerializer'] = []

    authors: list['AuthorSerializer'] = []


from .Series import SeriesSerializer
from .Author import AuthorSerializer
from .Status import StatusSerializer
from .Chapter import NovelChapterSerializer
NovelSerializer.update_forward_refs()
