from pydantic import HttpUrl, Field

from ..models import Model, db
from .Chapter import NovelChapter, MangaChapter, AnimeChapter
from ..tools.ModelType import StatusType


class Novel(Model):
    _collection = db["Novel"]
    _primary_keys = ['name']
    _relationships = {
        "one_to_many": {
            "chapters": {"model": NovelChapter, "related_fields": ["name"], "sort_by": "number"}
        }
    }
    _parents = {}

    image: HttpUrl = Field(default="http://test.com")
    status: StatusType = Field(default=StatusType.coming_Soon)
    authors: list[str] = Field(default=[])


class Manga(Model):
    _collection = db["Manga"]
    _primary_keys = ['name']
    _relationships = {
        "one_to_many": {
            "chapters": {"model": MangaChapter, "related_fields": ["name"], "sort_by": "number"}
        }
    }
    _parents = {}

    image: HttpUrl = Field(default="http://test.com")
    status: StatusType = Field(default=StatusType.coming_Soon)
    authors: list[str] = Field(default=[])


class Anime(Model):
    _collection = db["Anime"]
    _primary_keys = ['name']
    _relationships = {
        "one_to_many": {
            "episodes": {"model": AnimeChapter, "related_fields": ["name"], "sort_by": "number"}
        }
    }
    _parents = {}

    image: HttpUrl = Field(default="http://test.com")
    status: StatusType = Field(default=StatusType.coming_Soon)
    authors: list[str] = Field(default=[])


class Series(Model):
    _collection = db["Series"]
    _primary_keys = ['name']
    _relationships = {
        "one_to_one": {
            "novel": {"model": Novel, "related_fields": ["name"]},
            "manga": {"model": Manga, "related_fields": ["name"]},
            "anime": {"model": Anime, "related_fields": ["name"]}
        }
    }
    _parents = {}

    other_names: str = Field(default="")
    tags: list[str] = Field(default=[])
    genres: list[str] = Field(default=[])


Novel.create_index()
Manga.create_index()
Anime.create_index()
Series.create_index()
