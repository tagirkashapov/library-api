from app.models import Author
from app.repositories.base import BaseRepository
from app.schemas import AuthorResponse, AuthorCreate, AuthorUpdate


class AuthorRepository(
    BaseRepository[Author, AuthorResponse, AuthorCreate, AuthorUpdate]
):
    model = Author
    response_schema = AuthorResponse
