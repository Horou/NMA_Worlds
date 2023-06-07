from django.db import models

from NMA_Worlds.models import Model


class Genre(Model):
    pass


class Tag(Model):
    pass


class Status(Model):
    pass


class Author(Model):
    source = models.URLField(null=True)
    image = models.URLField(null=True)
