clickhouse_create_table = """
    CREATE TABLE IF NOT EXISTS video_quality
    (
        id UUID DEFAULT generateUUIDv4(),
        user_id UUID,
        timestamp DateTime64(6),
        film_id UUID,
        old_resolution UInt32,
        new_resolution UInt32
    )
    ENGINE = MergeTree()
    PRIMARY KEY id;
"""

vertica_create_table = """
    CREATE TABLE IF NOT EXISTS video_quality
    (
        id VARCHAR(36) DEFAULT MD5(RANDOM()::VARCHAR),
        user_id UUID,
        timestamp TIMESTAMP,
        film_id UUID,
        old_resolution INTEGER,
        new_resolution INTEGER
    )
    SEGMENTED BY HASH(id) ALL NODES;
"""

drop_table = "DROP TABLE IF EXISTS video_quality"

insert_query = """
    INSERT INTO video_quality
    (
        user_id,
        timestamp,
        film_id,
        old_resolution,
        new_resolution
    )
    VALUES
"""

select_query = "SELECT * FROM video_quality LIMIT {} OFFSET {}"

select_film_id_query = (
    "SELECT film_id FROM video_quality ORDER BY {} LIMIT {}"
)
