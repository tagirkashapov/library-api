from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload

from app.models import Book, Author, Publisher
from app.repositories.base import BaseRepository
from app.schemas import (
    BookResponse, BookDetailResponse, BookCreate, BookUpdate
)


class BookRepository(
    BaseRepository[Book, BookResponse, BookCreate, BookUpdate]
):
    model = Book
    response_schema = BookResponse

    async def _load_authors(self, author_ids: list[int]) -> list[Author]:
        authors = (await self.db.scalars(
            select(Author).where(Author.id.in_(author_ids))
        )).all()
        return list(authors)

    async def get_by_id(self, book_id: int) -> BookDetailResponse | None:
        self.logger.debug("Selecting Book record with id=%s", book_id)
        stmt = select(Book).where(Book.id == book_id).options(
            joinedload(Book.publisher).load_only(Publisher.id, Publisher.name),
            selectinload(Book.authors).load_only(Author.id, Author.name)
        )
        book = (await self.db.scalars(stmt)).unique().one_or_none()
        if book is None:
            return None
        return BookDetailResponse.model_validate(book)
    
    async def create(self, create_data: BookCreate) -> BookResponse:
        self.logger.debug("Inserting new Book record")
        book = Book(**create_data.model_dump(exclude={"author_ids"}))
        authors = await self._load_authors(create_data.author_ids)
        book.authors = authors
        self.db.add(book)
        await self.db.flush()
        await self.db.refresh(book)
        return BookResponse.model_validate(book)

    async def update(
        self, book_id: int, update_data: BookUpdate
    ) -> BookResponse | None:
        self.logger.debug("Updating Book record id=%s", book_id)
        book = await self.db.get(
            Book, book_id, options=[selectinload(Book.authors)]
        )
        if book is None:
            return None
        data = update_data.model_dump(exclude_unset=True)
        author_ids = data.pop("author_ids", None)
        for key, value in data.items():
            setattr(book, key, value)
        if author_ids is not None:
            book.authors = await self._load_authors(author_ids)
        await self.db.flush()
        await self.db.refresh(book)
        return BookResponse.model_validate(book)
