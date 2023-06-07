from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from ..models import Model

from .Tag import Genre, Tag
from .ManyToMany import tag_in_series, genre_in_series
from .Novel import Novel
from .Manga import Manga
from .Anime import Anime


class Series(Model):
    __tablename__ = "series"

    name = Column(String(100), nullable=False, primary_key=True)
    other_names = Column(String, nullable=True)
    description = Column(String, nullable=True)

    tags = relationship(Tag, secondary=lambda: tag_in_series, lazy="selectin")
    genres = relationship(Genre, secondary=lambda: genre_in_series, lazy="selectin")

    novel = relationship(Novel, uselist=False, back_populates='series', lazy="selectin")
    manga = relationship(Manga, uselist=False, back_populates='series', lazy="selectin")
    anime = relationship(Anime, uselist=False, back_populates='series', lazy="selectin")
