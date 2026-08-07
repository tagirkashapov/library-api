from sqlalchemy.orm import Session

from app.core.exceptions import EntityNotFound, NoFieldsToUpdate
from app.repositories import PublisherRepository
from app.schemas import (
    PublisherResponse, PublisherCreate, PublisherUpdate
)


class PublisherService:
    def __init__(self, db: Session):
        self.db = db
        self.publisher_repository = PublisherRepository(db)

    def get_publishers(self) -> list[PublisherResponse]:
        publishers = self.publisher_repository.get_all()
        return [
            PublisherResponse.model_validate(publisher)
            for publisher in publishers
        ]
    
    def get_publisher(self, publisher_id: int) -> PublisherResponse:
        publisher = self.publisher_repository.get_by_id(publisher_id)
        if publisher is None:
            return EntityNotFound("Publisher", publisher_id)
        return PublisherResponse.model_validate(publisher)

    def create_publisher(
        self, publisher_create: PublisherCreate
    ) -> PublisherResponse:
        publisher = self.publisher_repository.create(
            publisher_create.model_dump()
        )
        self.db.commit()
        return PublisherResponse.model_validate(publisher)

    def update_publisher(
        self, publisher_id: int, publisher_update: PublisherUpdate
    ) -> PublisherResponse:
        update_data = publisher_update.model_dump(exclude_unset=True)
        if not update_data:
            raise NoFieldsToUpdate("publisher")
        publisher = self.publisher_repository.update(publisher_id, update_data)
        if publisher is None:
            return EntityNotFound("Publisher", publisher_id)
        self.db.commit()
        return PublisherResponse.model_validate(publisher)

    def delete_publisher(self, publisher_id: int) -> None:
        deleted = self.publisher_repository.delete(publisher_id)
        if not deleted:
            return EntityNotFound("Publisher", publisher_id)
        self.db.commit()
