from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict, PositiveInt


class PublisherBase(BaseModel):
    name: str = Field(min_length=1, max_length=128)

    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)


class PublisherResponse(PublisherBase):
    id: PositiveInt
    created_at: datetime
    updated_at: datetime


class PublisherCreate(PublisherBase):
    pass


class PublisherUpdate(PublisherBase):
    name: str | None = Field(default=None, min_length=1, max_length=128)
