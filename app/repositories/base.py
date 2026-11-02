from typing import TypeVar, Generic, ClassVar
import logging

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db import Base

ModelT = TypeVar("ModelT", bound=Base)
ResponseT = TypeVar("ResponseT", bound=BaseModel)
CreateT = TypeVar("CreateT", bound=BaseModel)
UpdateT = TypeVar("UpdateT", bound=BaseModel)


class BaseRepository(Generic[ModelT, ResponseT, CreateT, UpdateT]):
    model: ClassVar[type[ModelT]]
    response_schema: ClassVar[type[ResponseT]]
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.logger = logging.getLogger(type(self).__module__)

    @property
    def entity_name(self) -> str:
        return self.model.__name__

    async def get_all(self) -> list[ResponseT]:
        self.logger.debug(
            "Selecting all %s records", self.entity_name
        )
        entities = (await self.db.scalars(select(self.model))).all()
        return [
            self.response_schema.model_validate(entity) for entity in entities
        ]

    async def get_by_id(self, entity_id: int) -> ResponseT | None:
        self.logger.debug(
            "Selecting %s record with id=%s", self.entity_name, entity_id
        )
        entity = await self.db.get(self.model, entity_id)
        if entity is None:
            return None
        return self.response_schema.model_validate(entity)

    async def create(self, create_data: CreateT) -> ResponseT:
        self.logger.debug("Inserting new %s record", self.entity_name)
        entity = self.model(**create_data.model_dump())
        self.db.add(entity)
        await self.db.flush()
        return self.response_schema.model_validate(entity)
    
    async def update(
        self, entity_id: int, update_data: UpdateT
    ) -> ResponseT | None:
        self.logger.debug(
            "Updating %s record id=%s", self.entity_name, entity_id
        )
        entity = await self.db.get(self.model, entity_id)
        if entity is None:
            return None
        for key, value in update_data.model_dump(exclude_unset=True).items():
            setattr(entity, key, value)
        await self.db.flush()
        await self.db.refresh(entity)
        return self.response_schema.model_validate(entity)

    async def delete(self, entity_id: int) -> bool:
        self.logger.debug(
            "Deleting %s record id=%s", self.entity_name, entity_id
        )
        entity = await self.db.get(self.model, entity_id)
        if entity is None:
            return False
        await self.db.delete(entity)
        await self.db.flush()
        return True
