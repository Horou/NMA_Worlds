from fastapi import APIRouter, HTTPException

from ..tools.ModelType import SortingType
from ..serializers.Series import Series, ReadSeries, Novel, ReadNovel, Manga, ReadManga, Anime, ReadAnime

series_router = APIRouter()


@series_router.get("/Search", response_model=list[ReadSeries], response_description="Search")
async def search_series(sort: str = "name",
                        order: SortingType = SortingType.ascending,
                        depth: int = 3,
                        filter_field: str = None,
                        filter_value: str = None,
                        page: int = 1,
                        size: int = 1000
                        ):
    filter_by = {filter_field: filter_value} if filter_field else {}
    sort_by = [(sort, int(order.value))] if sort else "name"
    if results := await Series.get_all(filter_by, sort_by=sort_by, depth=depth, page_num=page, page_size=size):
        return results
    raise HTTPException(status_code=404, detail=f"No {Series.__name__} instances found")


@series_router.get("/{series_name}", response_model=ReadSeries, response_description="Series Retrieved")
async def get_series(series_name: str):
    filter_by = {"name": series_name}
    if result := await Series.get(filter_by, depth=2):
        return result
    raise HTTPException(status_code=404, detail=f"{Series.__name__}: {filter_by} not found")


@series_router.post("/{series_name}", response_model=ReadSeries, response_description="Series Created")
async def create_series(series_name: str, series: Series):
    filter_by = {"name": series_name}
    if result := await series.create(filter_by, series.dict()):
        return result
    raise HTTPException(status_code=422, detail=f"{series.__class__.__name__}: {filter_by} already exist")


@series_router.put("/{series_name}", response_model=ReadSeries, response_description="Series Updated")
async def update_series(series_name: str, series: Series):
    filter_by = {"name": series_name}
    if result := await series.update(filter_by, series.dict()):
        return result
    raise HTTPException(status_code=422, detail=f"Failed to update {series.__class__.__name__}: {filter_by}")


@series_router.delete("/{series_name}", response_model=ReadSeries, response_description="Series Deleted")
async def delete_series(series_name: str):
    filter_by = {"name": series_name}
    if result := await Series.delete(filter_by):
        return result
    raise HTTPException(status_code=422, detail=f"Failed to delete {Series.__name__}: {filter_by}")


novel_router = APIRouter()


@novel_router.get("/Search", response_model=list[ReadNovel], response_description="Search")
async def search_novel(sort: str = "name",
                       order: SortingType = SortingType.ascending,
                       depth: int = 2,
                       filter_field: str = None,
                       filter_value: str = None,
                       page: int = 1,
                       size: int = 1000
                       ):
    filter_by = {filter_field: filter_value} if filter_field else {}
    sort_by = [(sort, int(order.value))] if sort else "name"
    if results := await Novel.get_all(filter_by, sort_by, depth=depth, page_num=page, page_size=size):
        return results
    raise HTTPException(status_code=404, detail=f"No {Novel.__name__} instances found")


@novel_router.get("/{novel_name}", response_model=ReadNovel, response_description="Novel Retrieved")
async def get_novel(novel_name: str):
    filter_by = {"name": novel_name}
    if result := await Novel.get(filter_by, depth=2):
        return result
    raise HTTPException(status_code=404, detail=f"{Novel.__name__}: {filter_by} not found")


@novel_router.post("/{novel_name}", response_model=ReadNovel, response_description="Novel Created")
async def create_novel(novel_name: str, novel: Novel):
    filter_by = {"name": novel_name}
    if result := await novel.create(filter_by, novel.dict()):
        return result
    raise HTTPException(status_code=422, detail=f"{novel.__class__.__name__}: {filter_by} already exist")


@novel_router.put("/{novel_name}", response_model=ReadNovel, response_description="Novel Updated")
async def update_novel(novel_name: str, novel: Novel):
    filter_by = {"name": novel_name}
    if result := await novel.update(filter_by, novel.dict()):
        return result
    raise HTTPException(status_code=422, detail=f"Failed to update {novel.__class__.__name__}: {filter_by}")


@novel_router.delete("/{novel_name}", response_model=bool, response_description="Novel Deleted")
async def delete_novel(novel_name: str):
    filter_by = {"name": novel_name}
    if result := await Novel.delete(filter_by):
        return result
    raise HTTPException(status_code=422, detail=f"Failed to delete {Novel.__name__}: {filter_by}")


manga_router = APIRouter()


@manga_router.get("/Search", response_model=list[ReadManga], response_description="Search")
async def search_manga(sort: str = "name",
                       order: SortingType = SortingType.ascending,
                       depth: int = 2,
                       filter_field: str = None,
                       filter_value: str = None,
                       page: int = 1,
                       size: int = 1000
                       ):
    filter_by = {filter_field: filter_value} if filter_field else {}
    sort_by = [(sort, int(order.value))] if sort else "name"
    if results := await Manga.get_all(filter_by, sort_by, depth=depth, page_num=page, page_size=size):
        return results
    raise HTTPException(status_code=404, detail=f"No {Manga.__name__} instances found")


@manga_router.get("/{manga_name}", response_model=ReadManga, response_description="Manga Retrieved")
async def get_manga(manga_name: str):
    filter_by = {"name": manga_name}
    if result := await Manga.get(filter_by, depth=2):
        return result
    raise HTTPException(status_code=404, detail=f"{Manga.__name__}: {filter_by} not found")


@manga_router.post("/{manga_name}", response_model=ReadManga, response_description="Manga Created")
async def create_manga(manga_name: str, manga: Manga):
    filter_by = {"name": manga_name}
    if result := await manga.create(filter_by, manga.dict()):
        return result
    raise HTTPException(status_code=422, detail=f"{manga.__class__.__name__}: {filter_by} already exist")


@manga_router.put("/{manga_name}", response_model=ReadManga, response_description="Manga Updated")
async def update_manga(manga_name: str, manga: Manga):
    filter_by = {"name": manga_name}
    if result := await manga.update(filter_by, manga.dict()):
        return result
    raise HTTPException(status_code=422, detail=f"Failed to update {manga.__class__.__name__}: {filter_by}")


@manga_router.delete("/{manga_name}", response_model=bool, response_description="Manga Deleted")
async def delete_manga(manga_name: str):
    filter_by = {"name": manga_name}
    if result := await Manga.delete(filter_by):
        return result
    raise HTTPException(status_code=422, detail=f"Failed to delete {Manga.__name__}: {filter_by}")


anime_router = APIRouter()


@anime_router.get("/Search", response_model=list[ReadAnime], response_description="Search")
async def search_anime(sort: str = "name",
                       order: SortingType = SortingType.ascending,
                       depth: int = 2,
                       filter_field: str = None,
                       filter_value: str = None,
                       page: int = 1,
                       size: int = 1000
                       ):
    filter_by = {filter_field: filter_value} if filter_field else {}
    sort_by = [(sort, int(order.value))] if sort else "name"
    if results := await Anime.get_all(filter_by, sort_by, depth=depth, page_num=page, page_size=size):
        return results
    raise HTTPException(status_code=404, detail=f"No {Anime.__name__} instances found")


@anime_router.get("/{anime_name}", response_model=ReadAnime, response_description="Anime Retrieved")
async def get_anime(anime_name: str):
    filter_by = {"name": anime_name}
    if result := await Anime.get(filter_by, depth=2):
        return result
    raise HTTPException(status_code=404, detail=f"{Anime.__name__}: {filter_by} not found")


@anime_router.post("/{anime_name}", response_model=ReadAnime, response_description="Anime Created")
async def create_anime(anime_name: str, anime: Anime):
    filter_by = {"name": anime_name}
    if result := await anime.create(filter_by, anime.dict()):
        return result
    raise HTTPException(status_code=422, detail=f"{anime.__class__.__name__}: {filter_by} already exist")


@anime_router.put("/{anime_name}", response_model=ReadAnime, response_description="Anime Updated")
async def update_anime(anime_name: str, anime: Anime):
    filter_by = {"name": anime_name}
    if result := await anime.update(filter_by, anime.dict()):
        return result
    raise HTTPException(status_code=422, detail=f"Failed to update {anime.__class__.__name__}: {filter_by}")


@anime_router.delete("/{anime_name}", response_model=bool, response_description="Anime Deleted")
async def delete_anime(anime_name: str):
    filter_by = {"name": anime_name}
    if result := await Anime.delete(filter_by):
        return result
    raise HTTPException(status_code=422, detail=f"Failed to delete {Anime.__name__}: {filter_by}")
