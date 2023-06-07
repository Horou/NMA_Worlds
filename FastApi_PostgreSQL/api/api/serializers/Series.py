from ..models.Series import Series
from ..serializers import Serializer

from .Tag import TagSerializer, GenreSerializer


class SeriesSerializer(Serializer):
    class Meta:
        orm_model = Series

    name: str
    other_names: str = None
    description: str = None

    tags: list[TagSerializer] = []
    genres: list[GenreSerializer] = []

    novel: 'NovelSerializer' = None
    manga: 'MangaSerializer' = None
    anime: 'AnimeSerializer' = None


from .Novel import NovelSerializer
from .Manga import MangaSerializer
from .Anime import AnimeSerializer
SeriesSerializer.update_forward_refs()
