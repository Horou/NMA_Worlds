from common.views import DeepViewset

from NMA_Worlds.models.Series import Novel, Manga, Anime, Series
from NMA_Worlds.models.Chapter import NovelChapter, MangaChapter, AnimeChapter
from NMA_Worlds.models.Other import Tag, Genre, Status, Author


class NovelViewSet(DeepViewset):
    queryset = Novel.objects


class MangaViewSet(DeepViewset):
    queryset = Manga.objects


class AnimeViewSet(DeepViewset):
    queryset = Anime.objects


class SeriesViewSet(DeepViewset):
    queryset = Series.objects


class NovelChapterViewSet(DeepViewset):
    queryset = NovelChapter.objects


class MangaChapterViewSet(DeepViewset):
    queryset = MangaChapter.objects


class AnimeChapterViewSet(DeepViewset):
    queryset = AnimeChapter.objects


class TagViewSet(DeepViewset):
    queryset = Tag.objects


class GenreViewSet(DeepViewset):
    queryset = Genre.objects


class StatusViewSet(DeepViewset):
    queryset = Status.objects


class AuthorViewSet(DeepViewset):
    queryset = Author.objects
