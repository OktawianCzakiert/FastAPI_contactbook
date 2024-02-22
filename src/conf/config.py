import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from icecream import ic


DOTENV = os.path.join(os.path.dirname(__file__), ".env")
print(DOTENV)


class Settings(BaseSettings):
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_port: int = 5432
    sqlalchemy_database_url: str
    scheme: str
    secret_key: str
    algorithm: str
    mail_username: str
    mail_password: str
    mail_from: str
    mail_port: int = 587
    mail_server: str = 'smtp.gmail.com'
    mail_from_name: str
    mail_starttls: bool = True
    mail_ssl_tls: bool = False
    use_credentials: bool = True
    validate_certs: bool = True
    redis_host: str = 'localhost'
    redis_port: int = 6379
    cloudinary_name: str
    cloudinary_api_key: str
    cloudinary_api_secret: str

    model_config = SettingsConfigDict(env_file=DOTENV)


settings = Settings()

# ic(settings.dict())
