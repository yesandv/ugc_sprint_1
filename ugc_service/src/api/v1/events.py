from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from ugc_service.src.schemas.event import EventType, Event
from ugc_service.src.services.event import EventService, get_event_service
from ugc_service.src.utils.jwt import security_jwt

router = APIRouter(prefix="/api/v1/events", tags=["EventService"])


@router.post(
    "",
    status_code=HTTPStatus.CREATED,
    description="Create a record of a user's activity",
)
async def record_event(
        event_type: EventType,
        event: Event,
        event_service: EventService = Depends(get_event_service),
        token: dict = Depends(security_jwt),  # noqa
):
    try:
        user_id = token.get("user_id")
        await event_service.record(user_id, event_type, event)
    except AssertionError:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)
