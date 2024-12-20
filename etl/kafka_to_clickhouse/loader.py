from clickhouse_driver import Client
from clickhouse_driver.errors import NetworkError

from etl.kafka_to_clickhouse.core.logger import logger
from etl.kafka_to_clickhouse.core.registry import query_registry
from etl.kafka_to_clickhouse.core.settings import settings


class ClickhouseLoader:

    def __init__(self):
        self.client = Client(**settings.clickhouse_config)

    def load_data(
            self,
            table_name: str,
            transformed_data: list[tuple],
    ):
        try:
            if table_name not in self.client.execute("SHOW TABLES"):
                self.client.execute(query_registry[table_name]["create"])
            num_columns = len(transformed_data[0])
            placeholders = "(" + ", ".join(["'{}'"] * num_columns) + ")"
            values = ", ".join(
                placeholders.format(*record) for record in transformed_data
            )
            self.client.execute(
                query_registry[table_name]["insert"].format(table_name, values)
            )
            logger.info(
                "Data has been loaded to Clickhouse, "
                "table: '%s', rows inserted: %d",
                table_name,
                len(transformed_data),
            )
        except NetworkError:
            logger.error("Check the connection")
