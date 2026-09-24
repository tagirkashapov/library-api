from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class PublisherBase(BaseModel):
    name: str = Field(min_length=1, max_length=128)

    model_config = ConfigDict(
        from_attributes=True,
        str_strip_whitespace=True,
        json_schema_extra={"example": {"name": "Publisher Name"}}
    )


class PublisherResponse(PublisherBase):
    id: int = Field(ge=1)
    created_at: datetime
    updated_at: datetime


class PublisherShortResponse(PublisherBase):
    id: int = Field(ge=1)


class PublisherCreate(PublisherBase):
    pass


class PublisherUpdate(PublisherBase):
    name: str | None = Field(None, min_length=1, max_length=128)
