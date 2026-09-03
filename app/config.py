from enum import Enum
from pydantic import PostgresDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class EnvEnum(str, Enum):
    DEV = "development"
    PROD = "production"
    TEST = "testing"

class Settings(BaseSettings):
    APP_NAME: str
    ENVIRONMENT: EnvEnum=EnvEnum.DEV
    PORT: int

    DATABASE_URL:PostgresDsn
    API_KEY: SecretStr
    model_config= SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )

settings = Settings()
