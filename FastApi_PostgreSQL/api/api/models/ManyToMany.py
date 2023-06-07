from sqlalchemy import Table, ForeignKey, Column, String

from ..models import Model

author_in_novel = Table(
    "author_in_novel",
    Model.metadata,
    Column("author_name", String(50), ForeignKey("authors.name"), primary_key=True),
    Column("novel_name", String(100), ForeignKey("novels.name"), primary_key=True),
)


author_in_manga = Table(
    "author_in_manga",
    Model.metadata,
    Column("author_name", String(50), ForeignKey("authors.name"), primary_key=True),
    Column("manga_name", String(100), ForeignKey("mangas.name"), primary_key=True),
)


author_in_anime = Table(
    "author_in_anime",
    Model.metadata,
    Column("author_name", String(50), ForeignKey("authors.name"), primary_key=True),
    Column("anime_name", String(100), ForeignKey("animes.name"), primary_key=True),
)


tag_in_series = Table(
    "tag_in_series",
    Model.metadata,
    Column("tag_name", String(20), ForeignKey("tags.name"), primary_key=True),
    Column("series_name", String(100), ForeignKey("series.name"), primary_key=True),
)


genre_in_series = Table(
    "genre_in_series",
    Model.metadata,
    Column("genre_name", String(20), ForeignKey("genres.name"), primary_key=True),
    Column("series_name", String(100), ForeignKey("series.name"), primary_key=True),
)

