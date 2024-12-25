from abc import ABC
from enum import StrEnum
from typing import Union
from uuid import UUID

from pydantic import BaseModel


class EventType(StrEnum):
    CLICK = "click"
    PAGE_VIEW = "page view"
    VIDEO_QUALITY = "video quality"
    COMPLETION = "completion"
    SEARCH = "search"


class BaseEvent(ABC, BaseModel):
    pass


class ClickEvent(BaseEvent):
    dom_element: str


class PageViewEvent(BaseEvent):
    url: str
    duration_sec: int


class VideoQualityEvent(BaseEvent):
    film_id: UUID
    old_resolution: int
    new_resolution: int


class CompletionEvent(BaseEvent):
    film_id: UUID


class Filter(StrEnum):
    FILM = "film"
    GENRE = "genre"
    PERSON = "person"


class SearchEvent(BaseEvent):
    filter: Filter
    query: str


Event = Union[
    ClickEvent, PageViewEvent, VideoQualityEvent, CompletionEvent, SearchEvent
]
