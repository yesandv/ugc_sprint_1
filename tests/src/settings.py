from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    clickhouse_host: str = "localhost"
    clickhouse_port: int = 9000
    clickhouse_db: str = "docker"
    clickhouse_user: str = "dbadmin"
    clickhouse_password: str = ""
    vertica_host: str = "localhost"
    vertica_port: int = 5433
    vertica_db: str = "docker"
    vertica_user: str = "dbadmin"
    vertica_password: str = ""
    batch_size: int = 1000
    num_records: int = 1000000

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
    def vertica_config(self) -> dict:
        return {
            "host": self.vertica_host,
            "port": self.vertica_port,
            "database": self.vertica_db,
            "user": self.vertica_user,
            "password": self.vertica_password,
            "autocommit": True,
            "tlsmode": "disable",
        }

    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / ".env", extra="ignore"
    )


test_settings = Settings()
