from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    stage: str = "dev"
    version: str = "0.0.1"
    sentry_dsn: str = ""
