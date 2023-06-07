from enum import Enum
from pymongo import ASCENDING, DESCENDING


class NovelChapterType(str, Enum):
    novel = "Novel"
    webnovel = "WebNovel"


class MangaChapterType(str, Enum):
    manga = "Manga"
    manhwa = "Manhwa"
    cg = "CG"


class AnimeChapterType(str, Enum):
    episode = "Episode"
    film = "Film"


class StatusType(str, Enum):
    ongoing = "Ongoing"
    completed = "Completed"
    hiatus = "Hiatus"
    dropped = "Dropped"
    coming_Soon = "Coming_Soon"


class SortingType(str, Enum):
    ascending = ASCENDING
    descending = DESCENDING
