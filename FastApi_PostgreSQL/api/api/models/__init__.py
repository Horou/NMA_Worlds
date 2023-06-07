from typing import Optional

from sqlalchemy.orm import declarative_base
from sqlalchemy.sql.expression import update as query_update
from sqlalchemy.sql.expression import delete as query_delete
from sqlalchemy.sql.expression import select as query_select
from sqlalchemy.sql.expression import and_

from ..database import db


class Model(declarative_base()):
    __abstract__ = True
    session = db
    models = {}
    validated = False

    def __init_subclass__(cls, *args, **kwargs):
        cls.models[f"{cls.__name__}"] = cls
        super().__init_subclass__(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        for key, relationship in self.__mapper__.relationships.items():
            data = kwargs.pop(key, None)
            if isinstance(data, list):
                setattr(self, key, [relationship.mapper.entity(**item) for item in data])
            elif isinstance(data, dict):
                setattr(self, key, relationship.mapper.entity(**data))
            elif data is not None:
                kwargs[key] = data
        super().__init__(*args, **kwargs)

    def dict(self):
        def _dict(instance: Model):
            data = instance.__dict__
            for key in instance.__mapper__.relationships.keys():
                field = data.pop(key, None)
                if isinstance(field, Model):
                    data[key] = _dict(field)
                elif isinstance(field, list):
                    data[key] = [_dict(child) for child in field]
            return data
        return _dict(self)

    @classmethod
    async def commit(cls):
        try:
            await cls.session.commit()
        except Exception:
            await cls.session.rollback()
            raise

    @classmethod
    async def _merge(cls, data):
        if isinstance(data, list):
            return [await cls._merge(child) for child in data]
        if isinstance(data, dict):
            model_name = data.pop("__model__", None)
            if model_name in cls.models:
                model = cls.models[model_name]
                instance = await cls.session.merge(model(**data))
                print(instance)
                return instance
            return {column: await cls._merge(child) for column, child in data.items()}
        return data

    @classmethod
    async def merge(cls, data):
        instances = await cls._merge(data)
        await cls.commit()
        return instances

    @classmethod
    async def create(cls, data) -> 'Model':
        instance = cls(**data)
        cls.session.add(instance)
        await cls.commit()
        return instance

    @classmethod
    async def get(cls, filters: dict) -> Optional['Model']:
        instances = await cls.session.get(cls, filters)
        return instances.scalar()

    @classmethod
    async def select(cls, filters: dict) -> Optional['Model']:
        instances = await cls.session.execute(
            query_select(cls)
            .where(and_(*[getattr(cls, key) == value for key, value in filters.items()]))
        )
        return instances.scalar()

    @classmethod
    async def get_all(cls, filters: dict, skip: int = 0, limit: int = 100) -> list['Model']:
        instances = await cls.session.execute(
            query_select(cls)
            .where(and_(*[getattr(cls, key) == value for key, value in filters.items()]))
            .offset(skip)
            .limit(limit)
        )
        return instances.scalars().all()

    @classmethod
    async def update(cls, filters: dict, data) -> 'Model':
        instances = await cls.session.get(cls, filters)
        instance = instances.scalar()
        instance.__dict__.update(data)
        await cls.commit()
        return instances.scalars().all()

    @classmethod
    async def update_query(cls, filters: dict, data) -> 'Model':
        instances = await cls.session.execute(
            query_update(cls)
            .where(and_(*[getattr(cls, key) == value for key, value in filters.items()]))
            .values(**data)
            .returning(cls)
        )
        await cls.commit()
        return await cls.get(filters) if instances.scalar() else None

    @classmethod
    async def delete(cls, filters: dict):
        instances = await cls.session.get(cls, filters)
        await cls.session.delete(instances)
        await cls.commit()
        return True

    @classmethod
    async def delete_query(cls, filters: dict) -> bool:
        await cls.session.execute(
            query_delete(cls)
            .where(and_(*[getattr(cls, key) == value for key, value in filters.items()]))
        )
        await cls.commit()
        return not (await cls.get(filters))

#
#
# @as_declarative
# class DefaultModel:
#     __abstract__ = True
#     models = {}
#
#     def __init_subclass__(cls, *args, **kwargs):
#         cls.models[f"{cls.__name__}"] = cls
#         super().__init_subclass__(*args, **kwargs)
#
#     def __repr__(self):
#         columns = ", ".join([f'{key}={value}' for key, value in self._dict().items()])
#         return f"<{self.__class__.__name__} ({columns})>"
#
#     def _dict(self):
#         return {col.name: str(getattr(self, col.name)) for col in self.__table__.columns}
#
#     @classmethod
#     def get_primary_keys(cls, data: dict) -> dict:
#         return {key: data.get(key) for key in inspect(cls).primary_key}
#
#     @staticmethod
#     async def commit():
#         try:
#             await db.commit()
#         except Exception:
#             await db.rollback()
#             raise
#
#     """                              QUERY                              """
#
#     @classmethod
#     def get_query(cls, filters: dict):
#         if not filters:
#             return select(cls)
#         return select(cls).where(and_(*[getattr(cls, key) == value for key, value in filters.items()]))
#
#     @classmethod
#     def update_query(cls, filters: dict, new_data: dict):
#         return query_update(cls) \
#             .where(and_(*[getattr(cls, key) == value for key, value in filters.items()])) \
#             .values(**new_data) \
#             .execution_options(synchronize_session="fetch")
#
#     @classmethod
#     def delete_query(cls, filters: dict):
#         return query_delete(cls) \
#             .where(and_(*[getattr(cls, key) == value for key, value in filters.items()]))
#
#     """                              GET CREATE UPDATE DELETE                              """
#
#     @classmethod
#     async def get(cls, filters: dict):
#         return await db.execute(cls.get_query(filters))
#
#     @classmethod
#     async def create(cls, data: dict):
#         instance = await db.merge(cls(**data))
#         await cls.commit()
#         return instance
#
#     @classmethod
#     async def update(cls, ids: dict, data: dict):
#         await db.execute(cls.update_query(ids, data))
#         await cls.commit()
#         return await cls.get(ids)
#
#     @classmethod
#     async def delete(cls, ids: dict):
#         await db.execute(cls.delete_query(ids))
#         await cls.commit()
#         return True
#
#     """                              MULTIPLE CREATE UPDATE DELETE                              """
#
#     @classmethod
#     async def get_all(cls, filters: dict = None):
#         query = cls.get_query(filters) if filters else select(cls)
#         instances = await db.execute(query)
#         return instances.scalars().all()
#
#     @classmethod
#     def create_model(cls, data: dict):
#         instance = cls(**data)
#         db.add(instance)
#         return instance
#
#     @classmethod
#     def create_or_update(cls, data: list | dict):
#         ids = cls.get_primary_keys(data)
#         new_data = {key: data[key] for key in cls.__table__.columns.keys() if key not in ids}
#         instance = cls.get(ids)
#         verified_instance = cls.update_model(ids, new_data) if instance else cls.create_model(data)
#         return verified_instance
#
#     @classmethod
#     def update_model(cls, ids: dict, data: dict):
#         query = cls.update_query(ids, data)
#         db.execute(query)
#         return cls.get(ids)
#
#     @classmethod
#     async def update_all(cls, data: list | dict):
#         instances = cls.update_deep(data)
#         await cls.commit()
#         return instances
#
#     @classmethod
#     async def delete_all(cls, data: list | dict):
#         instances = cls.delete_deep(data)
#         await cls.commit()
#         return instances
