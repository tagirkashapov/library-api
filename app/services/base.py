from typing import TypeVar, Generic, ClassVar
import logging

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import EntityNotFound, NoFieldsToUpdate
from app.db import Base
from app.repositories import BaseRepository

ModelT = TypeVar("ModelT", bound=Base)
ResponseT = TypeVar("ResponseT", bound=BaseModel)
CreateT = TypeVar("CreateT", bound=BaseModel)
UpdateT = TypeVar("UpdateT", bound=BaseModel)


class BaseService(Generic[ResponseT, CreateT, UpdateT]):
    repository_class: ClassVar[
        BaseRepository[ModelT, ResponseT, CreateT, UpdateT]
    ]

    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository: BaseRepository[
            ModelT, ResponseT, CreateT, UpdateT
        ] = self.repository_class(db)
        self.logger = logging.getLogger(type(self).__module__)

    @property
    def entity_name(self) -> str:
        return self.repository.model.__name__

    async def get_all(self) -> list[ResponseT]:
        self.logger.debug("Fetching all %s", self.entity_name)
        return await self.repository.get_all()

    async def get_by_id(self, entity_id: int) -> ResponseT:
        self.logger.debug(
            "Fetching %s with id=%s", self.entity_name, entity_id
        )
        entity = await self.repository.get_by_id(entity_id)
        if entity is None:
            self.logger.warning(
                "%s with id=%s not found",
                self.entity_name,
                entity_id
            )
            raise EntityNotFound(self.entity_name, entity_id)
        return entity

    async def create(self, create_data: CreateT) -> ResponseT:
        self.logger.info("Creating new %s", self.entity_name)
        entity = await self.repository.create(create_data)
        await self.db.commit()
        self.logger.info(
            "%s with id=%s created successfully",
            self.entity_name,
            getattr(entity, "id")
        )
        return entity

    async def update(self, entity_id: int, update_data: UpdateT) -> ResponseT:
        self.logger.info(
            "Updating %s with id=%s", self.entity_name, entity_id
        )
        if not update_data.model_fields_set:
            self.logger.warning(
                "No fields provided for %s update",
                self.entity_name
            )
            raise NoFieldsToUpdate(self.entity_name)
        entity = await self.repository.update(entity_id, update_data)
        if entity is None:
            self.logger.warning(
                "%s with id=%s not found",
                self.entity_name,
                entity_id
            )
            raise EntityNotFound(self.entity_name, entity_id)
        await self.db.commit()
        self.logger.info(
            "%s with id=%s updated successfully", self.entity_name, entity_id
        )
        return entity

    async def delete(self, entity_id: int) -> None:
        self.logger.info(
            "Deleting %s with id=%s", self.entity_name, entity_id
        )
        deleted = await self.repository.delete(entity_id)
        if not deleted:
            self.logger.warning(
                "%s with id=%s not found",
                self.entity_name,
                entity_id
            )
            raise EntityNotFound(self.entity_name, entity_id)
        await self.db.commit()
        self.logger.info(
            "%s with id=%s deleted successfully", self.entity_name, entity_id
        )
