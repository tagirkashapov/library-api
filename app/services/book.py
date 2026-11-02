from sqlalchemy.ext.asyncio import AsyncSession

from app.core import EntityNotFound, NoFieldsToUpdate
from app.repositories import (
    BookRepository, PublisherRepository, AuthorRepository
)
from app.schemas import (
    BookResponse, BookDetailResponse, BookCreate, BookUpdate
)
from app.services.base import BaseService

class BookService(
    BaseService[BookResponse, BookCreate, BookUpdate]
):
    repository_class = BookRepository
    repository: BookRepository

    def __init__(self, db: AsyncSession):
        super().__init__(db)
        self.publisher_repository = PublisherRepository(db)
        self.author_repository = AuthorRepository(db)

    async def get_by_id(self, entity_id: int) -> BookDetailResponse:
        self.logger.debug("Fetching Book with id=%s", entity_id)
        entity = await self.repository.get_by_id(entity_id)
        if entity is None:
            self.logger.warning("Book with id=%s not found", entity_id)
            raise EntityNotFound(self.entity_name, entity_id)
        return entity

    async def create(self, create_data: BookCreate) -> BookResponse:
        self.logger.info("Creating new Book")
        publisher_id = create_data.publisher_id
        publisher = await self.publisher_repository.get_by_id(
            publisher_id
        )
        if not publisher:
            self.logger.warning(
                "Publisher with id=%s not found",
                publisher_id
            )
            raise EntityNotFound("Publisher", publisher_id)
        author_ids = create_data.author_ids
        authors = await self.author_repository.get_by_ids(author_ids)
        missing = set(author_ids) - {author.id for author in authors}
        if missing:
            self.logger.warning("Author(s) with id(s)=%s not found", missing)
            raise EntityNotFound("Author", missing)
        entity = await self.repository.create(create_data)
        await self.db.commit()
        self.logger.info("Book with id=%s created successfully", entity.id)
        return entity
    
    async def update(
        self, entity_id: int, update_data: BookUpdate
    ) -> BookResponse:
        self.logger.info("Updating Book with id=%s", entity_id)
        if not update_data.model_fields_set:
            self.logger.warning("No fields provided for Book update")
            raise NoFieldsToUpdate(self.entity_name)
        publisher_id = update_data.publisher_id
        publisher = await self.publisher_repository.get_by_id(
            publisher_id
        )
        if not publisher:
            self.logger.warning(
                "Publisher with id=%s not found",
                publisher_id
            )
            raise EntityNotFound("Publisher", publisher_id)
        author_ids = update_data.author_ids
        authors = await self.author_repository.get_by_ids(author_ids)
        missing = set(author_ids) - {author.id for author in authors}
        if missing:
            self.logger.warning("Author(s) with id(s)=%s not found", missing)
            raise EntityNotFound("Author", missing)
        entity = await self.repository.update(entity_id, update_data)
        if entity is None:
            self.logger.warning(
                "Book with id=%s not found", entity_id
            )
            raise EntityNotFound(self.entity_name, entity_id)
        await self.db.commit()
        self.logger.info(
            "Book with id=%s updated successfully", entity_id
        )
        return entity
