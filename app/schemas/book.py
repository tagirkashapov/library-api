from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator, PositiveInt

from app.schemas import AuthorResponse, PublisherResponse


class BookBase(BaseModel):
    title: str = Field(min_length=1, max_length=128)
    publication_year: int = Field(ge=1445, le=date.today().year)
    isbn: str = Field(min_length=13, max_length=13)

    @field_validator("isbn")
    @classmethod
    def validate_isbn(cls, v: str | None) -> str | None:
        if v is None:
            return None
        if not v.isdigit():
            raise ValueError("ISBN must contain only digits")
        total = sum((3 if i % 2 else 1) * int(d) for i, d in enumerate(v[:12]))
        check_digit = (10 - (total % 10)) % 10
        if check_digit != int(v[12]):
            raise ValueError("Invalid ISBN-13 checksum")
        return v

    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)


class BookResponse(BookBase):
    id: PositiveInt
    publisher_id: PositiveInt
    created_at: datetime
    updated_at: datetime


class BookDetailResponse(BookBase):
    id: PositiveInt
    publisher: PublisherResponse
    authors: list[AuthorResponse]
    created_at: datetime
    updated_at: datetime


class BookCreate(BookBase):
    publisher_id: PositiveInt
    author_ids: list[PositiveInt]


class BookUpdate(BookBase):
    title: str | None = Field(default=None, min_length=1, max_length=128)
    publication_year: int | None = Field(
        default=None, ge=1445, le=date.today().year
    )
    isbn: str | None = Field(default=None, min_length=13, max_length=13)
    publisher_id: PositiveInt | None = None
    author_ids: list[PositiveInt] | None = None
