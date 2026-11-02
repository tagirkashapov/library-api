from typing import TYPE_CHECKING
from datetime import date, datetime

from pydantic import BaseModel, Field, field_validator, ConfigDict

if TYPE_CHECKING:
    from app.schemas import PublisherShortResponse
    from app.schemas import AuthorShortResponse


class BookBase(BaseModel):
    title: str = Field(min_length=1, max_length=128)
    publication_date: date = Field(ge=date(1970, 1, 1), le=date.today())
    isbn: str = Field(min_length=13, max_length=13)
    
    @field_validator("isbn")
    @classmethod
    def validate_isbn(cls, v: str | None) -> str | None:
        if v is None:
            return None
        if not v.isdigit():
            raise ValueError("ISBN must contain only digits")
        total = sum(
            (3 if i % 2 else 1) * int(digit) for i, digit in enumerate(v[:12])
        )
        check_digit = (10 - (total % 10)) % 10
        if check_digit != int(v[12]):
            raise ValueError("Invalid ISBN-13 checksum")
        return v
    
    model_config = ConfigDict(
        from_attributes=True,
        str_strip_whitespace=True,
        json_schema_extra={
            "example": {
                "title": "Book Title",
                "publication_date": "2000-01-01",
                "isbn": "9785948242736",
                "publisher_id": 1,
                "author_ids": [1, 2]
            }
        }
    )


class BookResponse(BookBase):
    id: int = Field(ge=1)
    created_at: datetime
    updated_at: datetime
    publisher_id: int


class BookDetailResponse(BookBase):
    id: int = Field(ge=1)
    created_at: datetime
    updated_at: datetime
    publisher: "PublisherShortResponse"
    authors: list["AuthorShortResponse"]


class BookCreate(BookBase):
    publisher_id: int
    author_ids: list[int]


class BookUpdate(BookBase):
    title: str | None = Field(None, min_length=1, max_length=128)
    publication_date: date | None = Field(
        None, ge=date(1970, 1, 1), le=date.today()
    )
    isbn: str | None = Field(None, min_length=13, max_length=13)
    publisher_id: int | None = None
    author_ids: list[int] | None = None


from app.schemas import AuthorShortResponse, PublisherShortResponse
BookDetailResponse.model_rebuild()
