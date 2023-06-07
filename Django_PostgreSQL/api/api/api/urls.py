"""
URL configuration for api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers
from NMA_Worlds.views import *

router = routers.DefaultRouter()
router.register(r'Novel', NovelViewSet)
router.register(r'Manga', MangaViewSet)
router.register(r'Anime', AnimeViewSet)
router.register(r'Series', SeriesViewSet)
router.register(r'NovelChapter', NovelChapterViewSet)
router.register(r'MangaChapter', MangaChapterViewSet)
router.register(r'AnimeChapter', AnimeChapterViewSet)
router.register(r'Tag', TagViewSet)
router.register(r'Genre', GenreViewSet)
router.register(r'Status', StatusViewSet)
router.register(r'Author', AuthorViewSet)

urlpatterns = [
    re_path(r'', include(router.urls)),
    path('admin/', admin.site.urls),
]
