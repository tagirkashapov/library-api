from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload, selectinload

from app.models import Book, Author


class BookRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, book_id: int) -> Book | None:
        return self.db.get(Book, book_id)

    def get_all_with_authors(self) -> list[Book]:
        stmt = select(Book).options(
            selectinload(Book.authors),
            joinedload(Book.publisher)
        )
        return self.db.scalars(stmt).unique().all()

    def get_by_id_with_authors(self, book_id: int) -> Book | None:
        stmt = select(Book).where(Book.id == book_id).options(
            selectinload(Book.authors),
            joinedload(Book.publisher)
        )
        return self.db.scalars(stmt).unique().first()

    def create(
        self, book_data: dict[str, Any], book_authors: list[Author]
    ) -> Book:
        new_book = Book(**book_data)
        new_book.authors = book_authors
        self.db.add(new_book)
        self.db.flush()
        return new_book

    def update(
        self,
        book_id: int,
        book_data: dict[str, Any],
        book_authors: list[Author]
    ) -> Book | None:
        book = self.get_by_id(book_id)
        if book is None:
            return book
        for key, value in book_data.items():
            setattr(book, key, value)
        book.authors = book_authors
        self.db.flush()
        return book

    def delete(self, book_id: int) -> True | False:
        book = self.get_by_id(book_id)
        if book is None:
            return False
        self.db.delete(book)
        self.db.flush()
        return True
