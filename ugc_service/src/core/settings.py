from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    project_name: str = "UGC Service"
    kafka_host: str = "localhost"
    kafka_port: int = 9092
    kafka_topic: str = "topic"
    jwt_secret_key: str = "secret"
    jwt_algorithm: str = ""

    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / ".env", extra="ignore"
    )


app_settings = Settings()
