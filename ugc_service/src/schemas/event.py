from abc import ABC
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel


class EventType(StrEnum):
    CLICK = "click"
    PAGE_VIEW = "page view"
    VIDEO_QUALITY = "video quality"
    COMPLETION = "completion"
    SEARCH = "search"


class Event(ABC, BaseModel):
    pass


class ClickEvent(Event):
    dom_element: str


class PageViewEvent(Event):
    url: str
    duration_sec: int


class VideoQualityEvent(Event):
    film_id: UUID
    old_resolution: int
    new_resolution: int


class CompletionEvent(Event):
    film_id: UUID


class Filter(StrEnum):
    FILM = "film"
    GENRE = "genre"
    PERSON = "person"


class SearchEvent(Event):
    filter: Filter
    query: str
