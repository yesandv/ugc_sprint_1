import sys
from itertools import groupby

if sys.version_info >= (3, 12, 0):
    import six

    sys.modules["kafka.vendor.six.moves"] = six.moves

from etl.kafka_to_clickhouse.consumer import Consumer
from etl.kafka_to_clickhouse.core.logger import logger
from etl.kafka_to_clickhouse.core.settings import settings
from etl.kafka_to_clickhouse.data_transformer import transform
from etl.kafka_to_clickhouse.loader import ClickhouseLoader


class ETLProcess:

    def __init__(self):
        self.consumer = Consumer(settings.kafka_topic)
        self.clickhouse_loader = ClickhouseLoader()
        self.batch = []

    def flush_batch(self):
        for table_name, data_group in groupby(self.batch, key=lambda x: x[0]):
            data_list = [data[1] for data in data_group]
            self.clickhouse_loader.load_data(table_name, data_list)
        self.consumer.kafka_consumer.commit()
        self.batch = []

    def run(self):
        logger.info("Starting the ETL process")
        try:
            for key, value in self.consumer.consume_messages():
                table_name = settings.event_type_map[key]
                transformed_data = transform(table_name, value)
                self.batch.append((table_name, transformed_data))

                if len(self.batch) >= settings.batch_size:
                    self.flush_batch()
        except KeyboardInterrupt:
            logger.info("Stopping the ETL process")
        finally:
            self.flush_batch()


if __name__ == "__main__":
    ETLProcess().run()
