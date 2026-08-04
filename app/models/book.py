from datetime import date

from sqlalchemy.orm import Mapped

from app.db.base import Base


class Book(Base):
    __tablename__ = "books"

    title: Mapped[str]
    author: Mapped[str]
    publisher: Mapped[str]
    publication_date: Mapped[date]
    isbn: Mapped[str]
