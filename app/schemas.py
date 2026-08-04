from datetime import date

from pydantic import BaseModel, Field, field_validator, model_validator


class BookBase(BaseModel):
    title: str = Field(min_length=1, max_length=128)
    author: str = Field(min_length=1, max_length=128)
    publisher: str = Field(min_length=1, max_length=128)
    publication_date: date = Field(ge=date(1970, 1, 1), le=date.today())
    isbn: str = Field(min_length=13, max_length=13)

    @field_validator("title", "author", "publisher", "isbn", mode="before")
    @classmethod
    def clean_string(cls, v: str | None) -> str | None:
        if isinstance(v, str):
            cleaned = v.strip()
            if not cleaned:
                raise ValueError("Field cannot be empty or contain only whitespace")
            return cleaned
        return v
    
    @field_validator("isbn")
    @classmethod
    def validate_isbn(cls, v: str) -> str:
        if not v.isdigit():
            raise ValueError("ISBN must contain only digits")
        total = sum((3 if i % 2 else 1) * int(digit) for i, digit in enumerate(v[:12]))
        check_digit = (10 - (total % 10)) % 10
        if check_digit != int(v[12]):
            raise ValueError("Invalid ISBN-13 checksum")
        return v
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "title",
                "author": "author",
                "publisher": "publisher",
                "publication_date": "2000-01-01",
                "isbn": "9785948242736"
            }
        }
    }


class BookResponse(BookBase):
    id: int = Field(ge=1)


class BookCreate(BookBase):
    pass


class BookUpdate(BookBase):
    title: str | None = Field(None, min_length=1, max_length=128)
    author: str | None = Field(None, min_length=1, max_length=128)
    publisher: str | None = Field(None, min_length=1, max_length=128)
    publication_date: date | None = Field(None, ge=date(1970, 1, 1), le=date.today())
    isbn: str | None = Field(None, min_length=13, max_length=13)
    
    @model_validator(mode="after")
    def validate_at_least_one_field(self) -> "BookUpdate":
        if all(value is None for value in self.__dict__.values()):
            raise ValueError("At least one field must be provided for update")
        return self
