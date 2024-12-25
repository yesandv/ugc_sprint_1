from datetime import datetime, UTC
from typing import TypeVar

from fastapi import Request

from ugc_service.src.core.settings import app_settings
from ugc_service.src.schemas.event import EventType, BaseEvent
from ugc_service.src.schemas.message import EventMessage
from ugc_service.src.services.broker import BaseBroker

T = TypeVar("T", bound=BaseEvent)


class EventService:

    def __init__(self, broker: BaseBroker):
        self.broker = broker

    async def record(self, user_id: str, event_type: EventType, event_body: T):
        msg = EventMessage(
            user_id=user_id,
            timestamp=datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S.%f"),
            event_body=event_body,
        )
        await self.broker.produce(
            app_settings.kafka_topic, event_type, msg.model_dump()
        )


def get_event_service(request: Request) -> EventService:
    return EventService(request.app.state.kafka)
