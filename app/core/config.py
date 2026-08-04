from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


def get_settings():
    return Settings()
