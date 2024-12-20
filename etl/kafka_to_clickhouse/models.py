from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, field_validator


class BaseEvent(BaseModel):
    user_id: UUID
    timestamp: datetime

    @field_validator("user_id", mode="before")  # noqa
    @classmethod
    def turn_str_into_uuid(cls, value):
        if isinstance(value, str):
            return UUID(value)
        return value

    @field_validator("timestamp", mode="before")  # noqa
    @classmethod
    def format_timestamp(cls, value):
        if isinstance(value, str):
            return datetime.strptime(value, "%Y-%m-%d %H:%M:%S.%f")
        return value


class ClickEvent(BaseEvent):
    dom_element: str


class PageViewEvent(BaseEvent):
    url: str
    duration_sec: int


class VideoQualityEvent(BaseEvent):
    film_id: UUID
    old_resolution: int
    new_resolution: int

    @field_validator("film_id", mode="before")  # noqa
    @classmethod
    def turn_str_into_uuid(cls, value):
        if isinstance(value, str):
            return UUID(value)
        return value


class CompletionEvent(BaseEvent):
    film_id: UUID

    @field_validator("film_id", mode="before")  # noqa
    @classmethod
    def turn_str_into_uuid(cls, value):
        if isinstance(value, str):
            return UUID(value)
        return value


class SearchEvent(BaseEvent):
    filter: str
    query: str
