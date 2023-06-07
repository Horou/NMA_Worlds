from pydantic import HttpUrl

from ..models.Author import Author

from ..serializers import Serializer
from .File import ImageSerializer


class AuthorSerializer(Serializer):
    class Meta:
        orm_model = Author

    name: str
    url: HttpUrl = None
    image_url: str = None

    image: ImageSerializer = None
    novels: list['NovelSerializer'] = []
    mangas: list['MangaSerializer'] = []
    animes: list['AnimeSerializer'] = []


from .Novel import NovelSerializer
from .Manga import MangaSerializer
from .Anime import AnimeSerializer
AuthorSerializer.update_forward_refs()
