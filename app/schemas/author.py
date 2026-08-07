from pydantic import (
    BaseModel, Field, field_validator, model_validator, ConfigDict
)


class AuthorBase(BaseModel):
    name: str = Field(min_length=1, max_length=128)

    @field_validator("name", mode="before")
    @classmethod
    def clean_string(cls, v: str | None) -> str | None:
        if isinstance(v, str):
            cleaned = v.strip()
            if not cleaned:
                raise ValueError(
                    "Field cannot be empty or contain only whitespace"
                )
            return cleaned
        return v
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={"example": {"name": "name"}}
    )


class AuthorResponse(AuthorBase):
    id: int = Field(ge=1)


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(AuthorBase):
    name: str | None = Field(None, min_length=1, max_length=128)
    
    @model_validator(mode="after")
    def validate_at_least_one_field(self) -> "AuthorUpdate":
        if not self.model_dump(exclude_unset=True):
            raise ValueError("At least one field must be provided for update")
        return self
