from typing import TYPE_CHECKING
from datetime import date

from sqlalchemy import Table, Column, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base
if TYPE_CHECKING:
    from app.models.author import Author
    from app.models.publisher import Publisher

book_authors = Table(
    "book_authors",
    Base.metadata,
    Column(
        "book_id",
        ForeignKey("books.id", ondelete="CASCADE"),
        primary_key=True
    ),
    Column(
        "author_id",
        ForeignKey("authors.id", ondelete="CASCADE"),
        primary_key=True
    )
)


class Book(Base):
    __tablename__ = "books"

    title: Mapped[str] = mapped_column(String(128))
    publication_date: Mapped[date]
    isbn: Mapped[str]= mapped_column(String(13))
    publisher_id: Mapped[int] = mapped_column(
        ForeignKey("publishers.id", ondelete="CASCADE"), nullable=True
    )

    publisher: Mapped["Publisher"] = relationship(back_populates="books")
    authors: Mapped[list["Author"]] = relationship(
        back_populates="books", secondary="book_authors"
    )
