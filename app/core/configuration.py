"""
    CONFIGURATION FILE
"""
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from pydantic import (
    AnyHttpUrl,
    BaseSettings,
    EmailStr,
    HttpUrl,
    PostgresDsn,
    validator,
)

from dotenv import load_dotenv

dotenv_path = Path(__file__).resolve().parent.parent.parent / ".env"

load_dotenv(dotenv_path)


class Settings(BaseSettings):
    """
    Class to contain the Settings for the application
    """

    API_V1_STR: str = os.environ.get("API_V1_STR")
    SECRET_KEY: str = os.environ.get("SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 90
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost",
        "http://localhost:4200",
        "http://localhost:3000",
        "http://localhost:8080",
    ]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(
        cls, value: Union[str, List[str]]
    ) -> Union[List[str], str]:
        """
        Method to Assemble cors origins
        """

        if isinstance(value, str) and not value.startswith("["):
            return [i.strip() for i in value.split(",")]
        if isinstance(value, (list, str)):
            return value
        raise ValueError(value)

    PROJECT_NAME: str = os.environ.get("PROJECT_NAME")
    POSTGRES_HOST: str = os.environ.get("POSTGRES_HOST")
    POSTGRES_USER: str = os.environ.get("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.environ.get("POSTGRES_PASSWORD")
    POSTGRES_DB: str = os.environ.get("POSTGRES_DB")
    POSTGRES_PORT: str = os.environ.get("POSTGRES_PORT")
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(
        cls, value: Optional[str], values: Dict[str, Any]
    ) -> Any:
        """
        Method to Assemble all db connection and return the connection
        """

        if isinstance(value, str):
            return value
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST"),
            port=values.get("POSTGRES_PORT"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    class Config:
        """
        Config class
        """

        case_sensitive = True


settings = Settings()
