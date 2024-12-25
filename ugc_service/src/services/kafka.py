import json

from aiokafka import AIOKafkaProducer

from ugc_service.src.core.encoder import UUIDEncoder
from ugc_service.src.services.broker import BaseBroker


class KafkaService(BaseBroker):
    def __init__(self, producer: AIOKafkaProducer):
        self.producer = producer

    async def produce(self, topic: str, key: str, body: dict):
        payload = json.dumps(body, cls=UUIDEncoder).encode("utf-8")
        await self.producer.send_and_wait(
            topic=topic,
            key=key.encode("utf-8"),
            value=payload,
        )
