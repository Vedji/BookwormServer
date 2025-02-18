from pydantic_settings import BaseSettings
from pydantic import Field, field_validator
from typing import Literal
from urllib.parse import urlparse


class Settings(BaseSettings):
    """Переменные окружения для сервера """

    # Общие переменные окружения
    ENVIRONMENT: Literal["development", "release"] = Field(default="development", validation_alias="ENVIRONMENT")
    SERVER_HOST: str = Field(default="0.0.0.0", validation_alias="SERVER_HOST")
    SERVER_PORT: int = Field(default=8000, validation_alias="SERVER_PORT")

    # Переменные окружения для авторизации на сервере
    JWT_SECRET_KEY: str = Field(..., validation_alias="JWT_SECRET_KEY")
    JWT_ALGORITHM: str = Field(default="HS256", validation_alias="JWT_ALGORITHM")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60, validation_alias="JWT_ACCESS_TOKEN_EXPIRE_MINUTES")

    # Переменные окружения для подключения к MySQL
    MYSQL_HOST: str = Field(default="localhost", validation_alias="MYSQL_HOST")
    MYSQL_PORT: int = Field(..., validation_alias="MYSQL_PORT")
    MYSQL_USER: str = Field(..., validation_alias="MYSQL_USER")
    MYSQL_PASSWORD: str = Field(..., validation_alias="MYSQL_PASSWORD")
    MYSQL_DBNAME: str = Field(..., validation_alias="MYSQL_DBNAME")

    # Переменные окружения для работы с S3-хранилищем
    S3_URL: str = Field(default="https://s3.amazonaws.com", validation_alias="S3_URL")
    S3_BUCKET_NAME: str = Field(..., validation_alias="S3_BUCKET_NAME")
    S3_ACCESS_KEY: str = Field(..., validation_alias="S3_ACCESS_KEY")
    S3_SECRET_ACCESS_KEY: str = Field(..., validation_alias="S3_SECRET_ACCESS_KEY")
    S3_REGION: str = Field(..., validation_alias="S3_REGION")
    S3_PROJECT_PREFIX: str = Field(..., validation_alias="S3_PROJECT_PREFIX")

    # Конфигурация .env
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def is_dev(self):
        return self.ENVIRONMENT == "development"

    @property
    def is_prod(self):
        return self.ENVIRONMENT == "release"

    # Валидация URL S3
    @field_validator("S3_URL", mode="before")
    def validate_s3_url(cls, v: str) -> str:
        parsed = urlparse(v)
        if not all([parsed.scheme, parsed.netloc]):
            raise ValueError(f"Некорректный URL для S3: {v}")
        return v

    # Валидация портов
    @field_validator("SERVER_PORT", "MYSQL_PORT")
    def validate_ports(cls, v: int) -> int:
        if not (1024 <= v <= 65535):
            raise ValueError(f"Некорректный порт: {v}. Допустимые значения: 1024-65535")
        return v

    # Валидация префикса S3
    @field_validator("S3_PROJECT_PREFIX")
    def validate_s3_prefix(cls, v: str) -> str:
        if not v.endswith("/"):
            raise ValueError(f"S3_PROJECT_PREFIX должен заканчиваться `/`, получено: {v}")
        return v



settings = Settings()
