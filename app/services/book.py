from sqlalchemy.orm import Session

from app.core.exceptions import NoFieldsToUpdate
from app.repositories.book import BookRepository
from app.schemas.book import BookResponse, BookCreate, BookUpdate


class BookService:
    def __init__(self, db: Session):
        self.db = db
        self.book_repository = BookRepository(db)

    def get_books(self) -> list[BookResponse]:
        books = self.book_repository.get_all()
        return [BookResponse.model_validate(book) for book in books]

    def get_book(self, book_id: int) -> BookResponse:
        book = self.book_repository.get_by_id(book_id)
        return BookResponse.model_validate(book)

    def create_book(self, book_create: BookCreate) -> BookResponse:
        book = self.book_repository.create(book_create.model_dump())
        self.db.commit()
        return BookResponse.model_validate(book)

    def update_book(
        self, book_id: int, book_update: BookUpdate
    ) -> BookResponse:
        update_data = book_update.model_dump(exclude_unset=True)
        if not update_data:
            raise NoFieldsToUpdate(f"No fields to update")
        book = self.book_repository.update(book_id, update_data)
        self.db.commit()
        return BookResponse.model_validate(book)

    def delete_book(self, book_id: int) -> None:
        self.book_repository.delete(book_id)
        self.db.commit()
