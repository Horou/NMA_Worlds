from datetime import datetime

from pydantic import BaseModel
from pymongo import ASCENDING

from ..database import client

db = client.nma_worlds


class Model(BaseModel):
    _collection = None
    _primary_keys = []
    _relationships = {}

    name: str
    description: str

    def __init_subclass__(cls, *args, **kwargs):
        super().__init_subclass__(*args, **kwargs)
        for _, rel in cls._relationships.get("one_to_one", {}).items():
            rel["model"]._parents[cls.__name__] = {"model": cls, "related_fields": rel["related_fields"]}
        for _, rel in cls._relationships.get("one_to_many", {}).items():
            rel["model"]._parents[cls.__name__] = {"model": cls, "related_fields": rel["related_fields"]}

    @classmethod
    async def get(cls, filters: dict, depth=1):
        if instance := await cls._collection.find_one(filters):
            return await cls._get_child(instance, depth=depth)
        return None

    @classmethod
    async def get_all(cls, filters: dict, sort_by: list[tuple], depth=1, page_size=1000, page_num=1):
        return [
            await cls._get_child(instance, depth=depth)
            async for instance in cls._collection.find(filters).sort(sort_by).skip(page_size * (page_num - 1)).limit(page_size)
        ]

    @classmethod
    async def _get_child(cls, data: dict, depth=1) -> dict:
        if depth := depth - 1:
            for output_field, rel in cls._relationships.get("one_to_one", {}).items():
                data[output_field] = await rel["model"].get(
                    {field: data[key] for field, key in zip(rel["related_fields"], cls._primary_keys)},
                    depth=depth
                )
            for output_field, rel in cls._relationships.get("one_to_many", {}).items():
                data[output_field] = await rel["model"].get_all(
                    {field: data[key] for field, key in zip(rel["related_fields"], cls._primary_keys)},
                    rel["sort_by"],
                    depth=depth
                )
            for output_field, rel in cls._relationships.get("many_to_many", {}).items():
                data[output_field] = await rel["model"].get_all(
                    {field: {"$all": [data[key]]} for field, key in zip(rel["related_fields"], cls._primary_keys)},
                    rel["sort_by"],
                    depth=depth
                )
        return data

    @classmethod
    async def create(cls, filters: dict, data: dict):
        if data := {k: filters[k] if k in filters else v for k, v in data.items()}:
            if not await cls.get(filters) and (result := await cls._collection.insert_one(cls._clean_data(data))):
                instance = await cls.get({"_id": result.inserted_id})
                child = await cls._create_child(data)
                for key, value in child.items():
                    instance[key] = value
                return instance
        return None

    @classmethod
    async def create_all(cls, filters: dict, list_data: list[dict], sort_by: list[tuple]):
        list_data = [
            {k: filters[k] if k in filters else v for k, v in data.items()}
            for data in list_data
            if not await cls.get({key: filters[key] if key in filters else data[key] for key in cls._primary_keys})
        ]
        to_insert = [cls._clean_data(data, create=True) for data in list_data]
        if list_data and (result := await cls._collection.insert_many(to_insert)):
            for data in list_data:
                await cls._create_child(data)
            return await cls.get_all(filters, sort_by, depth=4)
        return []

    @classmethod
    async def _create_child(cls, data: dict) -> dict:
        result = {}
        for output_field, rel in cls._relationships.get("one_to_one", {}).items():
            result[output_field] = await rel["model"].create(
                {field: data[key] for field, key in zip(rel["related_fields"], cls._primary_keys)},
                data[output_field]
            )
        for output_field, rel in cls._relationships.get("one_to_many", {}).items():
            result[output_field] = await rel["model"].create_all(
                {field: data[key] for field, key in zip(rel["related_fields"], cls._primary_keys)},
                data[output_field],
                rel["sort_by"]
            )
        return result

    @classmethod
    async def update(cls, filters: dict, data: dict):
        if data := {k: filters[k] if k in filters else v for k, v in data.items()}:
            result = await cls._collection.update_one(filters, {"$set": cls._clean_data(data)})
            if result.modified_count:
                instance = await cls.get(filters)
                await cls._update_parent(instance)
                return instance
        return None

    @classmethod
    async def update_all(cls, filters: dict, data: dict, sort_by: list[tuple]):
        if data := {k: filters[k] if k in filters else v for k, v in data.items()}:
            result = await cls._collection.update_many(filters, {"$set": cls._clean_data(data)})
            if result.modified_count:
                instances = await cls.get_all(filters, sort_by)
                for instance in instances:
                    await cls._update_parent(instance)
                return instances
        return []

    @classmethod
    async def _update_parent(cls, data: dict) -> bool:
        results = 0
        for name, parent in cls._parents.items():
            filter_by = {key: data[field] for key, field in zip(parent["model"]._primary_keys, parent["related_fields"])}
            results += int(bool(await parent["model"].update(filter_by, filter_by)))
        return True if results else False

    @classmethod
    async def delete(cls, filters: dict, cascade=True):
        if instance := await cls.get(filters):
            result = await cls._collection.delete_one(filters)
            if result.deleted_count:
                return await cls._delete_child(instance, cascade=cascade)
        return None

    @classmethod
    async def delete_all(cls, filters: dict, sort_by: list[tuple], cascade=True):
        if instances := await cls.get_all(filters, sort_by):
            result = await cls._collection.delete_many(filters)
            if result.deleted_count:
                return [await cls._delete_child(instance, cascade=cascade) for instance in instances]
        return []

    @classmethod
    async def _delete_child(cls, data: dict, cascade=True) -> dict:
        if cascade:
            for output_field, rel in cls._relationships.get("one_to_one", {}).items():
                filter_by = {field: data[key] for field, key in zip(rel["related_fields"], cls._primary_keys)}
                data[output_field] = await rel["model"].delete(filter_by, cascade=cascade)
            for output_field, rel in cls._relationships.get("one_to_many", {}).items():
                filter_by = {field: data[key] for field, key in zip(rel["related_fields"], cls._primary_keys)}
                data[output_field] = await rel["model"].delete_all(filter_by, rel["sort_by"], cascade=cascade)
        return data

    @classmethod
    def _clean_data(cls, data: dict, create=False):
        data["updated_at"] = datetime.now()
        if create:
            data["created_at"] = data["updated_at"]
        return {
            key: value
            for key, value in data.items()
            if value is not None and (
                    key not in cls._relationships.get("one_to_one", {}) or
                    key not in cls._relationships.get("one_to_many", {}) or
                    key not in cls._relationships.get("many_to_many", {})
            )
        }

    @classmethod
    def create_index(cls):
        cls._collection.create_index([(key, ASCENDING) for key in cls._primary_keys])
