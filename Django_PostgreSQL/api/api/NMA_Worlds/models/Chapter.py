from django.db import models

from NMA_Worlds.models import ChapterModel, Image, Video
from NMA_Worlds.models.Series import Novel, Manga, Anime


class NovelChapter(ChapterModel):
    novel = models.ForeignKey(Novel, related_name="chapters", on_delete=models.CASCADE, null=True)
    type = models.CharField(max_length=100, null=True)
    season = models.IntegerField(null=True)
    images = models.ManyToManyField(Image, blank=True)
    manga_chapter = models.ForeignKey("MangaChapter", on_delete=models.SET_NULL, null=True)
    anime_chapter = models.ForeignKey("AnimeChapter", on_delete=models.SET_NULL, null=True)
    source = models.URLField(null=True)


class MangaChapter(ChapterModel):
    manga = models.ForeignKey(Manga, related_name="chapters", on_delete=models.CASCADE, null=True)
    type = models.CharField(max_length=100, null=True)
    book = models.IntegerField(null=True)
    images = models.ManyToManyField(Image, blank=True)
    novel_chapter = models.ForeignKey(NovelChapter, on_delete=models.SET_NULL, null=True)
    anime_chapter = models.ForeignKey("AnimeChapter", on_delete=models.SET_NULL, null=True)
    source = models.URLField(null=True)


class AnimeChapter(ChapterModel):
    anime = models.ForeignKey(Anime, related_name="episodes", on_delete=models.CASCADE, null=True)
    type = models.CharField(max_length=100, null=True)
    season = models.IntegerField(null=True)
    videos = models.ManyToManyField(Video, blank=True)
    novel_chapter = models.ForeignKey(NovelChapter, on_delete=models.SET_NULL, null=True)
    manga_chapter = models.ForeignKey(MangaChapter, on_delete=models.SET_NULL, null=True)
    source = models.URLField(null=True)

