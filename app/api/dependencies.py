from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.db import get_db
from app.services import BookService, AuthorService, PublisherService


def get_book_service(db: Session = Depends(get_db)):
    return BookService(db)


def get_author_service(db: Session = Depends(get_db)):
    return AuthorService(db)


def get_publisher_service(db: Session = Depends(get_db)):
    return PublisherService(db)
