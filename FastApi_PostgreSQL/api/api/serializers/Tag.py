from ..models.Tag import Tag, Genre
from ..serializers import Serializer


class TagSerializer(Serializer):
    class Meta:
        orm_model = Tag

    name: str
    description: str = None


class GenreSerializer(Serializer):
    class Meta:
        orm_model = Genre

    name: str
    description: str = None
