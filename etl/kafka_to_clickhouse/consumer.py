import json

from kafka import KafkaConsumer
from kafka.protocol.message import Message

from etl.kafka_to_clickhouse.core.logger import logger
from etl.kafka_to_clickhouse.core.settings import settings


class Consumer:
    def __init__(self, topic: str):
        self.topic = topic
        self.kafka_consumer = KafkaConsumer(
            topic,
            bootstrap_servers=[f"{settings.kafka_host}:{settings.kafka_port}"],
            auto_offset_reset="earliest",
            group_id="etl_group",
            enable_auto_commit=False,
        )

    def consume_messages(self):
        try:
            while True:
                messages = self.kafka_consumer.poll(1)
                if not messages:
                    continue

                for partition, records in messages.items():
                    for record in records:
                        key, value = self.parse_message(record)
                        if key and value:
                            yield key, value

        except KeyboardInterrupt:
            logger.info("Stopping the consumer")
        finally:
            self.kafka_consumer.close()

    @staticmethod
    def parse_message(message: Message) -> tuple[str, dict]:
        try:
            key = message.key.decode("utf-8") if message.key else None
            value = message.value.decode("utf-8") if message.value else None
            return key, json.loads(value)
        except json.JSONDecodeError:
            logger.exception("Failed to parse the message: %s", message)
