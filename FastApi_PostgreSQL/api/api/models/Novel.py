from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from ..models import Model
from .ManyToMany import author_in_novel
from .File import Image
from .Status import Status
from .Chapter import NovelChapter
from .Author import Author


class Novel(Model):
    __tablename__ = "novels"

    name = Column(String(100), ForeignKey("series.name"), nullable=False, primary_key=True)
    image_url = Column(String(50), ForeignKey('images.url'), nullable=True)
    status_name = Column(String(10), ForeignKey("status.name"), nullable=True)

    series = relationship('Series', uselist=False, back_populates="novel", lazy="selectin")
    image = relationship(Image, uselist=False, lazy="selectin")
    status = relationship(Status, uselist=False, back_populates="novels", lazy="selectin")
    chapters = relationship(NovelChapter, back_populates="novel", lazy="selectin")

    authors = relationship(Author, secondary=lambda: author_in_novel, back_populates="novels", lazy="selectin")
