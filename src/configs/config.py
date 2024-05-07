from pathlib import Path

from itsdangerous import URLSafeTimedSerializer
from pydantic import BaseModel, PositiveInt
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent.parent


class DBSettings(BaseModel):
    URL: str


class CryptoSettings(BaseModel):
    PRIVATE_KEY_PATH: Path = BASE_DIR / "certs" / "private_key.pem"
    PUBLIC_KEY_PATH: Path = BASE_DIR / "certs" / "public_key.pem"
    ALGORITHM: str = "RS256"
    SECRET_KEY: str
    SALT_EMAIL_CONFIRMATION: str
    SALT_RESET_PASSWORD: str
    SALT_DEACTIVATE_ACCOUNT: str
    SALT_REACTIVATE_ACCOUNT: str


class TokenSettings(BaseModel):
    ACCESS_TOKEN_EXPIRE_MINUTES: PositiveInt = 15
    REFRESH_TOKNE_EXPIRE_DAYS: PositiveInt = 7


class CookieSettings(BaseModel):
    SECURE_FLAG: bool
    REFRESH_PATH: str = "/api/auth/refresh"
    LOGOUT_PATH: str = "/api/auth/logout"


class CelerySettings(BaseModel):
    BROKER_URL: str
    BACKEND: str


class FlowerSettings(BaseModel):
    BROKER_API: str
    ADDRESS: str
    PORT: int


class EmailSettings(BaseModel):
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_nested_delimiter="__")

    db: DBSettings
    crypto: CryptoSettings
    token: TokenSettings = TokenSettings()
    cookie: CookieSettings
    celery: CelerySettings
    flower: FlowerSettings
    email: EmailSettings

    SITE_DOMAIN: str
    FRONTEND_DOMAIN: str


settings = Settings()  # type: ignore

serializer = URLSafeTimedSerializer(settings.crypto.SECRET_KEY)
