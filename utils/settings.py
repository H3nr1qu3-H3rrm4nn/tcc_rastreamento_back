from enum import Enum
from urllib.parse import quote_plus

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings

class AppEnvironment(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"

class Settings(BaseSettings):

    APP_ENV: AppEnvironment = AppEnvironment.DEVELOPMENT

    USERNAME: str = Field(default="admin")
    PASSWORD: str = Field(default="tracking2025")
    HOST: str = Field(default="localhost")
    POSTGRES_PORT: int = Field(default=5432)
    DB_NAME: str = Field(default="tracker")
    DATABASE_URL: str | None = None

    SECRET_KEY: str = Field(default="")
    ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60)

    APP_NAME: str = Field(default="Rastreamento API")

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"

    @model_validator(mode="after")
    def _ensure_database_url(self):
        if not self.DATABASE_URL:
            encoded_password = quote_plus(self.PASSWORD)
            self.DATABASE_URL = (
                f"postgresql+asyncpg://{self.USERNAME}:{encoded_password}@"
                f"{self.HOST}:{self.POSTGRES_PORT}/{self.DB_NAME}"
            )

        if not self.SECRET_KEY:
            raise ValueError("SECRET_KEY must be provided via environment variable.")

        return self

settings = Settings()