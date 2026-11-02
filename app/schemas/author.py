from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class AuthorBase(BaseModel):
    name: str = Field(min_length=1, max_length=128)

    model_config = ConfigDict(
        from_attributes=True,
        str_strip_whitespace=True,
        json_schema_extra={"example": {"name": "Author Name"}}
    )


class AuthorResponse(AuthorBase):
    id: int = Field(ge=1)
    created_at: datetime
    updated_at: datetime


class AuthorShortResponse(AuthorBase):
    id: int = Field(ge=1)


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(AuthorBase):
    name: str | None = Field(None, min_length=1, max_length=128)
