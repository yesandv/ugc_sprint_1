from etl.kafka_to_clickhouse.core.settings import settings
from etl.kafka_to_clickhouse.models import (
    ClickEvent,
    PageViewEvent,
    VideoQualityEvent,
    CompletionEvent,
    SearchEvent,
)


def transform(table_name: str, msg: dict) -> tuple:
    event = None
    match table_name:
        case settings.click_table:
            event = ClickEvent(**msg, **msg.get("event_body"))
        case settings.page_view_table:
            event = PageViewEvent(**msg, **msg.get("event_body"))
        case settings.video_quality_table:
            event = VideoQualityEvent(**msg, **msg.get("event_body"))
        case settings.completion_table:
            event = CompletionEvent(**msg, **msg.get("event_body"))
        case settings.search_table:
            event = SearchEvent(**msg, **msg.get("event_body"))
    return tuple(event.model_dump().values())
