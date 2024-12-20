from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    kafka_host: str = "localhost"
    kafka_port: int = 9092
    kafka_topic: str = "topic"
    clickhouse_host: str = "localhost"
    clickhouse_port: int = 9000
    clickhouse_db: str = "docker"
    clickhouse_user: str = "dbadmin"
    clickhouse_password: str = ""
    click_table: str = "click_event"
    page_view_table: str = "page_view_event"
    video_quality_table: str = "video_quality_event"
    completion_table: str = "completion_event"
    search_table: str = "search_event"
    batch_size: int = 1000

    @property
    def clickhouse_config(self) -> dict:
        return {
            "host": self.clickhouse_host,
            "port": self.clickhouse_port,
            "database": self.clickhouse_db,
            "user": self.clickhouse_user,
            "password": self.clickhouse_password,
        }

    @property
    def event_type_map(self):
        return {
            "click": self.click_table,
            "page view": self.page_view_table,
            "video quality": self.video_quality_table,
            "completion": self.completion_table,
            "search": self.search_table,
        }

    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / ".env", extra="ignore"
    )


settings = Settings()
