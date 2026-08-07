from sqlalchemy.orm import Session

from app.core.exceptions import EntityNotFound, NoFieldsToUpdate

from app.repositories import BookRepository, AuthorRepository
from app.schemas import BookDetailResponse, BookCreate, BookUpdate


class BookService:
    def __init__(self, db: Session):
        self.db = db
        self.book_repository = BookRepository(db)
        self.author_repository = AuthorRepository(db)

    def get_books(self) -> list[BookDetailResponse]:
        books = self.book_repository.get_all_with_authors()
        return [BookDetailResponse.model_validate(book) for book in books]

    def get_book(self, book_id: int) -> BookDetailResponse:
        book = self.book_repository.get_by_id_with_authors(book_id)
        if book is None:
            raise EntityNotFound("Book", book_id)
        return BookDetailResponse.model_validate(book)

    def create_book(self, book_create: BookCreate) -> BookDetailResponse:
        book_data = book_create.model_dump()
        author_ids = book_data.pop("author_ids")
        authors = self.author_repository.get_by_ids(author_ids)
        book = self.book_repository.create(book_data, authors)
        self.db.commit()
        return BookDetailResponse.model_validate(book)

    def update_book(
        self, book_id: int, book_update: BookUpdate
    ) -> BookDetailResponse:
        update_data = book_update.model_dump(exclude_unset=True)
        if not update_data:
            raise NoFieldsToUpdate("book")
        author_ids = update_data.pop("author_ids")
        authors = self.author_repository.get_by_ids(author_ids)
        book = self.book_repository.update(book_id, update_data, authors)
        if book is None:
            raise EntityNotFound("Book", book_id)
        self.db.commit()
        return BookDetailResponse.model_validate(book)

    def delete_book(self, book_id: int) -> None:
        deleted = self.book_repository.delete(book_id)
        if not deleted:
            raise EntityNotFound("Book", book_id)
        self.db.commit()
