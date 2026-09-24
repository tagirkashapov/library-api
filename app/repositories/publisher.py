from app.models import Publisher
from app.repositories.base import BaseRepository
from app.schemas import PublisherResponse, PublisherCreate, PublisherUpdate


class PublisherRepository(
    BaseRepository[
        Publisher, PublisherResponse, PublisherCreate, PublisherUpdate
    ]
):
    model = Publisher
    response_schema = PublisherResponse
