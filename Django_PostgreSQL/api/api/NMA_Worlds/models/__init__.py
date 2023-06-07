import uuid

from django.db import models
from model_utils.managers import InheritanceManager


class Video(models.Model):
    objects = InheritanceManager()
    url = models.URLField(primary_key=True)


class Image(models.Model):
    objects = InheritanceManager()
    url = models.URLField(primary_key=True)


class Model(models.Model):
    class Meta:
        abstract = True

    objects = InheritanceManager()
    name = models.CharField(max_length=100, primary_key=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ChapterModel(models.Model):
    class Meta:
        abstract = True

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    objects = InheritanceManager()
    name = models.CharField(max_length=100)
    number = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
