from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Depends

from ugc_service.src.schemas.event import (
    ClickEvent,
    EventType,
    PageViewEvent,
    VideoQualityEvent,
    CompletionEvent,
    SearchEvent,
)
from ugc_service.src.services.event import EventService, get_event_service
from ugc_service.src.utils.jwt import security_jwt

router = APIRouter(prefix="/api/v1/events", tags=["EventService"])


@router.post(
    "/clicks",
    status_code=HTTPStatus.CREATED,
    description="Create a record of a user's click event",
)
def record_click_event(
        event: ClickEvent,
        event_service: EventService = Depends(get_event_service),
        token: dict = Depends(security_jwt),  # noqa
):
    try:
        user_id = token.get("user_id")
        event_service.record(user_id, EventType.CLICK, event)
    except AssertionError:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)


@router.post(
    "/page-views",
    status_code=HTTPStatus.CREATED,
    description="Create a record of a new page view and its duration",
)
def record_page_view_event(
        event: PageViewEvent,
        event_service: EventService = Depends(get_event_service),
        token: dict = Depends(security_jwt),  # noqa
):
    try:
        user_id = token.get("user_id")
        event_service.record(user_id, EventType.PAGE_VIEW, event)
    except AssertionError:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)


@router.post(
    "/video-quality-changes",
    status_code=HTTPStatus.CREATED,
    description="Create a record of a resolution change",
)
def record_video_quality_event(
        event: VideoQualityEvent,
        event_service: EventService = Depends(get_event_service),
        token: dict = Depends(security_jwt),  # noqa
):
    try:
        user_id = token.get("user_id")
        event_service.record(user_id, EventType.VIDEO_QUALITY, event)
    except AssertionError:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)


@router.post(
    "/film-completions",
    status_code=HTTPStatus.CREATED,
    description="Create a record of a completed film view",
)
def record_film_completion_event(
        event: CompletionEvent,
        event_service: EventService = Depends(get_event_service),
        token: dict = Depends(security_jwt),  # noqa
):
    try:
        user_id = token.get("user_id")
        event_service.record(user_id, EventType.COMPLETION, event)
    except AssertionError:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)


@router.post(
    "/searches",
    status_code=HTTPStatus.CREATED,
    description="Create a search record",
)
def record_search_event(
        event: SearchEvent,
        event_service: EventService = Depends(get_event_service),
        token: dict = Depends(security_jwt),  # noqa
):
    try:
        user_id = token.get("user_id")
        event_service.record(user_id, EventType.SEARCH, event)
    except AssertionError:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)
