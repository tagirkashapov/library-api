from app.repositories import PublisherRepository
from app.schemas import PublisherResponse, PublisherCreate, PublisherUpdate
from app.services.base import BaseService

class PublisherService(
    BaseService[PublisherResponse, PublisherCreate, PublisherUpdate]
):
    repository_class = PublisherRepository
