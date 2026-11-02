from sqlalchemy import select

from app.models import Author
from app.repositories.base import BaseRepository
from app.schemas import AuthorResponse, AuthorCreate, AuthorUpdate


class AuthorRepository(
    BaseRepository[Author, AuthorResponse, AuthorCreate, AuthorUpdate]
):
    model = Author
    response_schema = AuthorResponse

    async def get_by_ids(self, author_ids: list[int]) -> list[AuthorResponse]:
        self.logger.debug("Selecting Author records with ids=%s", author_ids)
        stmt = select(Author).where(Author.id.in_(author_ids))
        authors = (await self.db.scalars(stmt)).all()
        return [AuthorResponse.model_validate(author) for author in authors]
