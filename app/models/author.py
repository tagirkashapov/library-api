from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from app.db import Base


class Author(Base):
    __tablename__ = "authors"

    name: Mapped[str] = mapped_column(String(128))
