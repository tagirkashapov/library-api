from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from app.db import Base


class Publisher(Base):
    __tablename__ = "publishers"
    
    name: Mapped[str] = mapped_column(String(128))
