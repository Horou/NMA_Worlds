from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from ..models import Model


class Status(Model):
    __tablename__ = "status"
    name = Column(String(10), nullable=False, primary_key=True)
    description = Column(String, nullable=True)

    novels = relationship('Novel', back_populates="status", lazy="selectin")
    mangas = relationship('Manga', back_populates="status", lazy="selectin")
    animes = relationship('Anime', back_populates="status", lazy="selectin")
