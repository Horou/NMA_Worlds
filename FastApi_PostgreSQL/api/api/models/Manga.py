from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from ..models import Model
from .ManyToMany import author_in_manga
from .File import Image
from .Status import Status
from .Chapter import MangaChapter
from .Author import Author


class Manga(Model):
    __tablename__ = "mangas"

    name = Column(String(100), ForeignKey("series.name"), nullable=False, primary_key=True)
    image_url = Column(String(50), ForeignKey('images.url'), nullable=True)
    status_name = Column(String(10), ForeignKey("status.name"), nullable=True)

    series = relationship('Series', uselist=False, back_populates="manga", lazy="selectin")
    image = relationship(Image, uselist=False, lazy="selectin")
    status = relationship(Status, uselist=False, back_populates="mangas", lazy="selectin")
    chapters = relationship(MangaChapter, back_populates="manga", lazy="selectin")

    authors = relationship(Author, secondary=lambda: author_in_manga, back_populates="mangas", lazy="selectin")
