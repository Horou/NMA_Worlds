from sqlalchemy import Column, DateTime, String, Numeric, ForeignKey, SmallInteger
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ..models import Model

from .File import MangaPage, AnimeVideo


class NovelChapter(Model):
    __tablename__ = "novel_chapters"
    number = Column(Numeric(precision=1), nullable=False, primary_key=True)
    novel_name = Column(String(100), ForeignKey("novels.name"), nullable=False, primary_key=True)
    season = Column(SmallInteger, nullable=True)
    name = Column(String(50), nullable=True)
    release_date = Column(DateTime, default=func.now())

    content = Column(String, nullable=True)
    novel = relationship('Novel', back_populates="chapters", lazy="selectin")


class MangaChapter(Model):
    __tablename__ = "manga_chapters"
    number = Column(Numeric(precision=1), nullable=False, primary_key=True)
    manga_name = Column(String(100), ForeignKey("mangas.name"), nullable=False, primary_key=True)
    season = Column(SmallInteger, nullable=False)
    name = Column(String(50), nullable=True)
    release_date = Column(DateTime, default=func.now())

    content = relationship(MangaPage, lazy="selectin")
    manga = relationship('Manga', back_populates="chapters", lazy="selectin")


class AnimeChapter(Model):
    __tablename__ = "anime_chapters"
    number = Column(Numeric(precision=1), nullable=False, primary_key=True)
    anime_name = Column(String(100), ForeignKey("animes.name"), nullable=False, primary_key=True)
    season = Column(SmallInteger, nullable=False)
    name = Column(String(50), nullable=True)
    release_date = Column(DateTime, default=func.now())

    content = relationship(AnimeVideo, lazy="selectin")
    anime = relationship('Anime', back_populates="chapters", lazy="selectin")
