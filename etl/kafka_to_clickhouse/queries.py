create_click_table = """
    CREATE TABLE IF NOT EXISTS {}
    (
        id UUID DEFAULT generateUUIDv4(),
        user_id UUID,
        timestamp DateTime64,
        dom_element String
    )
    ENGINE = MergeTree()
    PRIMARY KEY id;
"""

create_page_view_table = """
    CREATE TABLE IF NOT EXISTS {}
    (
        id UUID DEFAULT generateUUIDv4(),
        user_id UUID,
        timestamp DateTime64,
        url String,
        duration_sec Int32
    )
    ENGINE = MergeTree()
    PRIMARY KEY id;
"""

create_video_quality_table = """
    CREATE TABLE IF NOT EXISTS {}
    (
        id UUID DEFAULT generateUUIDv4(),
        user_id UUID,
        timestamp DateTime64,
        film_id UUID,
        old_resolution Int32,
        new_resolution Int32
    )
    ENGINE = MergeTree()
    PRIMARY KEY id;
"""

create_completion_table = """
    CREATE TABLE IF NOT EXISTS {}
    (
        id UUID DEFAULT generateUUIDv4(),
        user_id UUID,
        timestamp DateTime64,
        film_id UUID
    )
    ENGINE = MergeTree()
    PRIMARY KEY id;
"""

create_search_table = """
    CREATE TABLE IF NOT EXISTS {}
    (
        id UUID DEFAULT generateUUIDv4(),
        user_id UUID,
        timestamp DateTime64,
        filter String,
        query String
    )
    ENGINE = MergeTree()
    PRIMARY KEY id;
"""

insert_click_event = (
    "INSERT INTO {} (user_id, timestamp, dom_element) VALUES {}"
)

insert_page_view_event = """
    INSERT INTO {}
    (
        user_id,
        timestamp,
        url,
        duration_sec
    )
    VALUES {}
"""

insert_video_quality_event = """
    INSERT INTO {}
    (
        user_id,
        timestamp,
        film_id,
        old_resolution,
        new_resolution
    )
    VALUES {}
"""

insert_completion_event = (
    "INSERT INTO {} (user_id, timestamp, film_id) VALUES {}"
)

insert_search_event = (
    "INSERT INTO {} (user_id, timestamp, filter, query) VALUES {}"
)
