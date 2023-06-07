from sqlalchemy import Column, String

from ..models import Model


class Tag(Model):
    __tablename__ = "tags"
    name = Column(String(20), nullable=False, primary_key=True)
    description = Column(String, nullable=True)


class Genre(Model):
    __tablename__ = "genres"
    name = Column(String(20), nullable=False, primary_key=True)
    description = Column(String, nullable=True)
