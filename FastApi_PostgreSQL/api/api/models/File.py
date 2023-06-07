from sqlalchemy import Column, ForeignKeyConstraint, String, SmallInteger, Numeric

from ..models import Model


class Image(Model):
    __tablename__ = "images"
    url = Column(String(200), nullable=False, primary_key=True)


class MangaPage(Model):
    __tablename__ = "manga_pages"
    number = Column(SmallInteger, nullable=False, primary_key=True)
    manga_name = Column(String(100), nullable=False, primary_key=True)
    chapter_number = Column(Numeric(precision=1), nullable=False, primary_key=True)

    url = Column(String(200), nullable=True)

    __table_args__ = (ForeignKeyConstraint((manga_name, chapter_number),
                                           ('manga_chapters.manga_name', 'manga_chapters.number')),)


class AnimeVideo(Model):
    __tablename__ = "anime_videos"
    number = Column(SmallInteger, nullable=False, primary_key=True)
    anime_name = Column(String(100), nullable=False, primary_key=True)
    chapter_number = Column(Numeric(precision=1), nullable=False, primary_key=True)

    url = Column(String(200), nullable=True)

    __table_args__ = (ForeignKeyConstraint((anime_name, chapter_number),
                                           ('anime_chapters.anime_name', 'anime_chapters.number')),)
