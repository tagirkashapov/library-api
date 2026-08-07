from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Publisher


class PublisherRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Publisher]:
        return self.db.scalars(select(Publisher)).all()

    def get_by_id(self, publisher_id) -> Publisher | None:
        return self.db.get(Publisher, publisher_id)

    def create(self, publisher_data: dict[str, Any]) -> Publisher:
        new_publisher = Publisher(**publisher_data)
        self.db.add(new_publisher)
        self.db.flush()
        return new_publisher

    def update(
        self, publisher_id: int, publisher_data: dict[str, Any]
    ) -> Publisher | None:
        publisher = self.get_by_id(publisher_id)
        if publisher is None:
            return None
        for key, value in publisher_data.items():
            setattr(publisher, key, value)
        self.db.flush()
        return publisher

    def delete(self, publisher_id: int) -> True | False:
        publisher = self.get_by_id(publisher_id)
        if publisher is None:
            return False
        self.db.delete(publisher)
        self.db.flush()
        return True
