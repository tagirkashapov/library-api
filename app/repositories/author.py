from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Author


class AuthorRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Author]:
        return self.db.scalars(select(Author)).all()

    def get_by_id(self, author_id: int) -> Author | None:
        return self.db.get(Author, author_id)

    def get_by_ids(self, author_ids: list[int]) -> list[Author]:
        return self.db.query(Author).filter(Author.id.in_(author_ids)).all()

    def create(self, author_data: dict[str, Any]) -> Author:
        new_author = Author(**author_data)
        self.db.add(new_author)
        self.db.flush()
        return new_author

    def update(
        self, author_id: int, author_data: dict[str, Any]
    ) -> Author | None:
        author = self.get_by_id(author_id)
        if author is None:
            return None
        for key, value in author_data.items():
            setattr(author, key, value)
        self.db.flush()
        return author

    def delete(self, author_id: int) -> True | False:
        author = self.get_by_id(author_id)
        if author is None:
            return False
        self.db.delete(author)
        self.db.flush()
        return True
