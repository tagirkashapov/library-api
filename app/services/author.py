from sqlalchemy.orm import Session

from app.core.exceptions import EntityNotFound, NoFieldsToUpdate
from app.repositories import AuthorRepository
from app.schemas import AuthorResponse, AuthorCreate, AuthorUpdate


class AuthorService:
    def __init__(self, db: Session):
        self.db = db
        self.author_repository = AuthorRepository(db)

    def get_authors(self) -> list[AuthorResponse]:
        authors = self.author_repository.get_all()
        return [AuthorResponse.model_validate(author) for author in authors]
    
    def get_author(self, author_id: int) -> AuthorResponse:
        author = self.author_repository.get_by_id(author_id)
        if author is None:
            raise EntityNotFound("Author", author_id)
        return AuthorResponse.model_validate(author)

    def create_author(self, author_create: AuthorCreate) -> AuthorResponse:
        author = self.author_repository.create(author_create.model_dump())
        self.db.commit()
        return AuthorResponse.model_validate(author)

    def update_author(
        self, author_id: int, author_update: AuthorUpdate
    ) -> AuthorResponse:
        update_data = author_update.model_dump(exclude_unset=True)
        if not update_data:
            raise NoFieldsToUpdate("author")
        author = self.author_repository.update(author_id, update_data)
        if author is None:
            raise EntityNotFound("Author", author_id)
        self.db.commit()
        return AuthorResponse.model_validate(author)

    def delete_author(self, author_id: int) -> None:
        deleted = self.author_repository.delete(author_id)
        if not deleted:
            raise EntityNotFound("Author", author_id)
        self.db.commit()
