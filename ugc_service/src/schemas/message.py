from typing import TypeVar

from pydantic import BaseModel, ConfigDict

from ugc_service.src.schemas.event import Event

T = TypeVar("T", bound=Event)


class EventMessage(BaseModel):
    user_id: str
    timestamp: str
    event_body: T

    model_config = ConfigDict(arbitrary_types_allowed=True)
