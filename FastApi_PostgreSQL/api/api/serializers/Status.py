from ..models.Status import Status
from ..serializers import Serializer


class StatusSerializer(Serializer):
    class Meta:
        orm_model = Status

    name: str
    description: str = None

    novels: list['NovelSerializer'] = []
    mangas: list['MangaSerializer'] = []
    animes: list['AnimeSerializer'] = []


from .Novel import NovelSerializer
from .Manga import MangaSerializer
from .Anime import AnimeSerializer
StatusSerializer.update_forward_refs()
