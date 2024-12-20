import json
import sys
from functools import lru_cache

from ugc_service.src.core.encoder import UUIDEncoder

if sys.version_info >= (3, 12, 0):
    import six

    sys.modules["kafka.vendor.six.moves"] = six.moves

from kafka import KafkaProducer
from ugc_service.src.core.settings import app_settings

from ugc_service.src.services.broker import BaseBroker


class KafkaService(BaseBroker):
    def __init__(self, producer: KafkaProducer):
        self.producer = producer

    def produce(self, topic: str, key: str, body: dict):
        payload = json.dumps(body, cls=UUIDEncoder).encode("utf-8")
        self.producer.send(
            topic=topic,
            key=key.encode("utf-8"),
            value=payload,
        )


@lru_cache()
def get_kafka_service():
    return KafkaService(
        KafkaProducer(
            bootstrap_servers=[
                f"{app_settings.kafka_host}:{app_settings.kafka_port}"
            ],
        )
    )
