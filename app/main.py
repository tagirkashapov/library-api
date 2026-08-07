from fastapi import FastAPI

from app.models import *
from app.schemas import (
    BookResponse, BookDetailResponse, AuthorResponse, PublisherResponse
)
from app.api.routers import *

BookResponse.model_rebuild()
BookDetailResponse.model_rebuild()
AuthorResponse.model_rebuild()
PublisherResponse.model_rebuild()

app = FastAPI()

app.include_router(book_router)
app.include_router(author_router)
app.include_router(publisher_router)
