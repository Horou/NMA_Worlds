from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from ..models import Model
from .ManyToMany import author_in_anime
from .File import Image
from .Status import Status
from .Chapter import AnimeChapter
from .Author import Author


class Anime(Model):
    __tablename__ = "animes"

    name = Column(String(100), ForeignKey("series.name"), nullable=False, primary_key=True)
    image_url = Column(String(50), ForeignKey('images.url'), nullable=True)
    status_name = Column(String(10), ForeignKey("status.name"), nullable=True)

    series = relationship('Series', uselist=False, back_populates="anime", lazy="selectin")
    image = relationship(Image, uselist=False, lazy="selectin")
    status = relationship(Status, uselist=False, back_populates="animes", lazy="selectin")
    chapters = relationship(AnimeChapter, back_populates="anime", lazy="selectin")

    authors = relationship(Author, secondary=lambda: author_in_anime, back_populates="animes", lazy="selectin")
