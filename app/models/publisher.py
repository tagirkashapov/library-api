from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

from app.db import Base
if TYPE_CHECKING:
    from app.models.book import Book


class Publisher(Base):
    __tablename__ = "publishers"
    
    name: Mapped[str] = mapped_column(String(128))

    books: Mapped[list["Book"]] = relationship(back_populates="publisher")
