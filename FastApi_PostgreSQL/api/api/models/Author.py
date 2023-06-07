from sqlalchemy import ForeignKey, Column, String
from sqlalchemy.orm import relationship

from ..models import Model
from .ManyToMany import author_in_novel, author_in_manga, author_in_anime


class Author(Model):
    __tablename__ = "authors"
    name = Column(String(50), nullable=False, primary_key=True)
    url = Column(String(100), nullable=True)
    image_url = Column(String(50), ForeignKey('images.url'), nullable=True)

    image = relationship('Image', uselist=False, lazy="selectin")
    novels = relationship('Novel', secondary=lambda: author_in_novel, back_populates="authors", lazy="selectin")
    mangas = relationship('Manga', secondary=lambda: author_in_manga, back_populates="authors", lazy="selectin")
    animes = relationship('Anime', secondary=lambda: author_in_anime, back_populates="authors", lazy="selectin")
