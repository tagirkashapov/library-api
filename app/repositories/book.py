from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exceptions import BookNotFound
from app.models.book import Book


class BookRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Book]:
        return self.db.scalars(select(Book)).all()

    def get_by_id(self, book_id: int) -> Book:
        book = self.db.get(Book, book_id)
        if not book:
            raise BookNotFound(f"Book with id {book_id} not found")
        return book

    def create(self, book_data: dict[str, Any]) -> Book:
        new_book = Book(**book_data)
        self.db.add(new_book)
        self.db.flush()
        return new_book

    def update(self, book_id: int, book_data: dict[str, Any]) -> Book:
        book = self.get_by_id(book_id)
        for key, value in book_data.items():
            setattr(book, key, value)
        self.db.flush()
        return book

    def delete(self, book_id: int) -> None:
        book = self.get_by_id(book_id)
        self.db.delete(book)
        self.db.flush()
