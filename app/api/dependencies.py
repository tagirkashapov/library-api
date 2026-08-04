from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.db import get_db
from app.services.book import BookService


def get_book_service(db: Session = Depends(get_db)):
    return BookService(db)
