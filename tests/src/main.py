import time
from concurrent.futures import ThreadPoolExecutor

import vertica_python
from clickhouse_driver import Client
from vertica_python import Connection

from tests.src.settings import test_settings
from tests.src.utils import queries
from tests.src.utils.data_helper import generate_data, join_values
from tests.src.utils.logging import logger
from tests.src.utils.mesure_time import timeit


@timeit("Clickhouse Insert")
def clickhouse_insert(client: Client, data: list[tuple]):
    for i in range(0, test_settings.num_records, test_settings.batch_size):
        batch = data[i:i + test_settings.batch_size]
        values = join_values(batch)
        client.execute(f"{queries.insert_query} {values}")


@timeit("Vertica Insert")
def vertica_insert(vertica_connection: Connection, data: list[tuple]):
    cursor = vertica_connection.cursor()
    for i in range(0, test_settings.num_records, test_settings.batch_size):
        batch = data[i:i + test_settings.batch_size]
        cursor.executemany(
            f"{queries.insert_query} (%s, %s, %s, %s, %s)", batch
        )


@timeit("Clickhouse Read")
def clickhouse_read(client: Client):
    for offset in range(
            0, test_settings.num_records, test_settings.batch_size
    ):
        client.execute(
            queries.select_query.format(test_settings.batch_size, offset)
        )


@timeit("Vertica Read")
def vertica_read(vertica_connection: Connection):
    cursor = vertica_connection.cursor()
    for offset in range(
            0, test_settings.num_records, test_settings.batch_size
    ):
        cursor.execute(
            queries.select_query.format(test_settings.batch_size, offset)
        )
        cursor.fetchall()


def clickhouse_realtime_insert(client: Client, duration: int = 30):
    start_time = time.monotonic()
    end_time = start_time + duration
    records_inserted = 0

    while time.monotonic() < end_time:
        data = generate_data(test_settings.batch_size)
        values = join_values(data)
        client.execute(f"{queries.insert_query} {values}")
        records_inserted += len(data)

    logger.info("Clickhouse total records inserted: %d", records_inserted)


def clickhouse_realtime_read(client: Client, duration: int = 30):
    start_time = time.monotonic()
    end_time = start_time + duration
    records_read = 0

    while time.monotonic() < end_time:
        aggregate_start_time = time.monotonic()

        result = client.execute(
            queries.select_film_id_query.format(
                "rand()", test_settings.batch_size
            )
        )
        records_read += len(result)

        aggregate_duration = time.monotonic() - aggregate_start_time

        if aggregate_duration > 10:
            logger.warning(
                "Clickhouse query exceeded 10 seconds. Duration: %.2f seconds",
                aggregate_duration,
            )
            break

    logger.info("Clickhouse total records read: %d", records_read)


def clickhouse_realtime(duration: int = 30):
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(
            clickhouse_realtime_insert,
            Client(**test_settings.clickhouse_config),
            duration,
        )
        executor.submit(
            clickhouse_realtime_read,
            Client(**test_settings.clickhouse_config),
            duration,
        )


def vertica_realtime_insert(
        vertica_connection: Connection, duration: int = 30
):
    start_time = time.monotonic()
    end_time = start_time + duration
    records_inserted = 0
    cursor = vertica_connection.cursor()

    while time.monotonic() < end_time:
        data = generate_data(test_settings.batch_size)
        cursor.executemany(
            f"{queries.insert_query} (%s, %s, %s, %s, %s)", data
        )
        records_inserted += len(data)

    logger.info("Vertica total records inserted: %d", records_inserted)


def vertica_realtime_read(
        vertica_connection: Connection, duration: int = 30
):
    start_time = time.monotonic()
    end_time = start_time + duration
    records_read = 0
    cursor = vertica_connection.cursor()

    while time.monotonic() < end_time:
        aggregate_start_time = time.monotonic()

        cursor.execute(
            queries.select_film_id_query.format(
                "RANDOM()", test_settings.batch_size
            )
        )
        result = cursor.fetchall()
        records_read += len(result)

        aggregate_duration = time.monotonic() - aggregate_start_time

        if aggregate_duration > 10:
            logger.warning(
                "Vertica query exceeded 10 seconds. Duration: %.2f seconds",
                aggregate_duration,
            )
            break

    logger.info("Vertica total records read: %d", records_read)


def vertica_realtime(duration: int = 30):
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(
            vertica_realtime_insert,
            vertica_python.connect(**test_settings.vertica_config),
            duration,
        )
        executor.submit(
            vertica_realtime_read,
            vertica_python.connect(**test_settings.vertica_config),
            duration,
        )


def main():
    clickhouse_client = Client(**test_settings.clickhouse_config)
    clickhouse_client.execute(queries.clickhouse_create_table)
    vertica_connection = vertica_python.connect(**test_settings.vertica_config)
    cursor = vertica_connection.cursor()
    cursor.execute(queries.vertica_create_table)
    data = generate_data(test_settings.num_records)
    try:
        clickhouse_insert(clickhouse_client, data)
        vertica_insert(vertica_connection, data)
        clickhouse_read(clickhouse_client)
        vertica_read(vertica_connection)
        clickhouse_realtime()
        vertica_realtime()
    finally:
        clickhouse_client.execute(queries.drop_table)
        cursor.execute(queries.drop_table)
        cursor.close()
        vertica_connection.close()


if __name__ == "__main__":
    main()
