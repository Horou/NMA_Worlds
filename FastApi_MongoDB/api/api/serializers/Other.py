from pydantic import Field

from ..models.Other import Genre, Tag, Status, Author
from .Series import ReadNovel, ReadManga, ReadAnime


class ReadGenre(Genre):
    pass


class ReadTag(Tag):
    pass


class ReadStatus(Status):
    novels: list[ReadNovel] = Field(default=[])
    mangas: list[ReadManga] = Field(default=[])
    animes: list[ReadAnime] = Field(default=[])


class ReadAuthor(Author):
    novels: list[ReadNovel] = Field(default=[])
    mangas: list[ReadManga] = Field(default=[])
    animes: list[ReadAnime] = Field(default=[])
