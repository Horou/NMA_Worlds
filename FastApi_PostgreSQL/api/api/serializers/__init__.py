from pydantic import BaseModel
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.main import validate_model

from ..models import Model


class Serializer(BaseModel):

    class Meta:
        orm_model: Model = None

    class Config:
        orm_mode = True

    @classmethod
    async def merge(cls, data):
        instances = await cls.Meta.orm_model.merge([item.dict() for item in data])
        return instances

    async def create(self):
        instance_data = self.dict()
        instance_data.pop("__model__", None)
        return await self.Meta.orm_model.create(instance_data)

    @classmethod
    async def get(cls, filters: dict):
        model = cls.Meta.orm_model
        instance = await model.session.get(model, filters)
        if not instance:
            raise HTTPException(status_code=404, detail=f"{model.__name__} not found")
        return instance

    @classmethod
    async def get_all(cls, filters: dict):
        instances = await cls.Meta.orm_model.get_all(filters)
        if not instances:
            raise HTTPException(status_code=404, detail=f"No {cls.Meta.orm_model.__name__} found")
        print("///////////////////////////////////////////////////////////////////////////////")
        print(instances)
        print([instance.__dict__ for instance in instances])
        return [instance.dict() for instance in instances]

    async def update(self, filters: dict):
        stored_item_data = await self.get(filters)
        for key, value in self.dict(exclude_unset=True).items():
            if issubclass(type(value), Serializer):
                value = value.update()
            setattr(stored_item_data, key, value)
        await self.Meta.orm_model.commit()
        return stored_item_data

    @classmethod
    async def delete(cls,  filters: dict):
        model = cls.Meta.orm_model
        stored_item_data = await cls.get(filters)


        await self.Meta.orm_model.commit()
        return stored_item_data

        deleted = await cls.Meta.orm_model.delete(filters)
        if not deleted:
            raise HTTPException(status_code=422, detail=f"Failed to delete")
        return deleted
