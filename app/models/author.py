from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import Base
if TYPE_CHECKING:
    from app.models import Book


class Author(Base):
    __tablename__ = "authors"
    
    name: Mapped[str] = mapped_column(String(128))

    books: Mapped[list["Book"]] = relationship(
        back_populates="authors", secondary="books_authors"
    )
