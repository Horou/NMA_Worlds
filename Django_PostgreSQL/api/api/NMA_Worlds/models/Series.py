from django.db import models

from NMA_Worlds.models import Model
from NMA_Worlds.models.Other import Status, Author, Tag, Genre


class Novel(Model):
    image = models.URLField(null=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True)
    authors = models.ManyToManyField(Author, related_name="novels", blank=True)


class Manga(Model):
    image = models.URLField(null=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True)
    authors = models.ManyToManyField(Author, related_name="mangas", blank=True)


class Anime(Model):
    image = models.URLField(null=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True)
    authors = models.ManyToManyField(Author, related_name="animes", blank=True)


class Series(Model):
    other_names = models.TextField(null=True)
    tags = models.ManyToManyField(Tag, related_name="series", blank=True)
    genres = models.ManyToManyField(Genre, related_name="series", blank=True)

    novel = models.OneToOneField(Novel, related_name="series", on_delete=models.CASCADE, null=True)
    manga = models.OneToOneField(Manga, related_name="series", on_delete=models.CASCADE, null=True)
    anime = models.OneToOneField(Anime, related_name="series", on_delete=models.CASCADE, null=True)
