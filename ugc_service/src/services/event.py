import sys
from datetime import datetime, UTC
from functools import lru_cache
from typing import TypeVar

from fastapi import Depends

from ugc_service.src.core.settings import app_settings
from ugc_service.src.schemas.event import EventType, Event
from ugc_service.src.schemas.message import EventMessage
from ugc_service.src.services.broker import BaseBroker
from ugc_service.src.services.kafka import get_kafka_service

T = TypeVar("T", bound=Event)


class EventService:

    def __init__(self, broker: BaseBroker):
        self.broker = broker

    def record(self, user_id: str, event_type: EventType, event_body: T):
        msg = EventMessage(
            user_id=user_id,
            timestamp=datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S.%f"),
            event_body=event_body,
        )
        self.broker.produce(
            app_settings.kafka_topic, event_type, msg.model_dump()
        )


@lru_cache()
def get_event_service(
        broker: BaseBroker = Depends(get_kafka_service)
):
    return EventService(broker)
