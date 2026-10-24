from typing import Literal

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    database_url: str


    jwt_secret_key: SecretStr
    jwt_algorithm: Literal["HS256"] = "HS256"
    access_token_expire_minutes: int = 10

    refresh_token_expire_days: int = 7


    refresh_cookie_name: str = "eir_refresh"
    refresh_cookie_secure: bool = False
    refresh_cookie_samesite: Literal["lax", "strict", "none"] = "lax"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    jwt_issuer: str = "eir-api"
    jwt_audience: str = "eir-web"
    csrf_cookie_name: str = "eir_csrf"
    csrf_header_name: str = "X-CSRF-Token"
    frontend_origins: list[str] = ["http://localhost:5000"]


settings = Settings()
