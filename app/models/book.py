from typing import TYPE_CHECKING
from datetime import date

from sqlalchemy import Table, Column, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import Base
if TYPE_CHECKING:
    from app.models import Author
    from app.models import Publisher

books_authors = Table(
    "books_authors",
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
    publish_date: Mapped[date]
    isbn: Mapped[str]= mapped_column(String(13))
    publisher_id: Mapped[int] = mapped_column(
        ForeignKey("publishers.id", ondelete="SET NULL"), nullable=True
    )

    publisher: Mapped["Publisher"] = relationship(back_populates="books")
    authors: Mapped[list["Author"]] = relationship(
        back_populates="books", secondary=books_authors
    )
