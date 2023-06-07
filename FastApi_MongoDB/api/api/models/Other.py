from pydantic import HttpUrl, Field

from ..models import Model, db
from .Series import Novel, Manga, Anime
from ..tools.ModelType import StatusType


class Genre(Model):
    _collection = db["Genre"]
    _primary_keys = ['name']
    _parents = {}


class Tag(Model):
    _collection = db["Tag"]
    _primary_keys = ['name']
    _parents = {}


class Status(Model):
    _collection = db["Status"]
    _primary_keys = ['name']
    _relationships = {
        "one_to_many": {
            "novels": {"model": Novel, "related_fields": ["status"], "sort_by": "name"},
            "mangas": {"model": Manga, "related_fields": ["status"], "sort_by": "name"},
            "animes": {"model": Anime, "related_fields": ["status"], "sort_by": "name"}
        }
    }
    _parents = {}

    name: StatusType = Field(default=StatusType.coming_Soon)


class Author(Model):
    _collection = db["Author"]
    _primary_keys = ['name']
    _relationships = {
        "many_to_many": {
            "novels": {"model": Novel, "related_fields": ["authors"], "sort_by": "name"},
            "mangas": {"model": Manga, "related_fields": ["authors"], "sort_by": "name"},
            "animes": {"model": Anime, "related_fields": ["authors"], "sort_by": "name"}
        }
    }
    _parents = {}

    source: HttpUrl | None = Field(default="http://test.com")
    image: HttpUrl | None = Field(default="http://test.com")


Genre.create_index()
Tag.create_index()
Status.create_index()
Author.create_index()
