from app.repositories import AuthorRepository
from app.schemas import AuthorResponse, AuthorCreate, AuthorUpdate
from app.services.base import BaseService

class AuthorService(
    BaseService[AuthorResponse, AuthorCreate, AuthorUpdate]
):
    repository_class = AuthorRepository
