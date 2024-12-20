from etl.kafka_to_clickhouse import queries
from etl.kafka_to_clickhouse.core.settings import settings

query_registry = {
    settings.click_table: {
        "create": queries.create_click_table.format(settings.click_table),
        "insert": queries.insert_click_event,
    },
    settings.page_view_table: {
        "create": queries.create_page_view_table.format(
            settings.page_view_table
        ),
        "insert": queries.insert_page_view_event,
    },
    settings.video_quality_table: {
        "create": queries.create_video_quality_table.format(
            settings.video_quality_table
        ),
        "insert": queries.insert_video_quality_event,
    },
    settings.completion_table: {
        "create": queries.create_completion_table.format(
            settings.completion_table
        ),
        "insert": queries.insert_completion_event,
    },
    settings.search_table: {
        "create": queries.create_search_table.format(settings.search_table),
        "insert": queries.insert_search_event,
    },
}
