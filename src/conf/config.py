from pydantic import ConfigDict, EmailStr
from pydantic_settings import BaseSettings

"""
Configuration settings for the application, loaded from environment variables.
"""


class Settings(BaseSettings):
    """
    Defines the application settings using Pydantic's BaseSettings.
    Values are loaded from environment variables and an optional .env file.
    """

    DB_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    JWT_EXPIRATION_SECONDS: int

    MAIL_USERNAME: EmailStr
    MAIL_PASSWORD: str
    MAIL_FROM: EmailStr
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str
    MAIL_STARTTLS: bool = False
    MAIL_SSL_TLS: bool = True
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True

    CLD_NAME: str
    CLD_API_KEY: int
    CLD_API_SECRET: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int

    model_config = ConfigDict(
        extra="ignore", env_file=".env", env_file_encoding="utf-8", case_sensitive=True
    )


settings = Settings()
