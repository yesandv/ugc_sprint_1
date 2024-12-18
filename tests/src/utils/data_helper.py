import random
from datetime import datetime, UTC
from uuid import uuid4

from tests.src.settings import test_settings


def generate_data(batch_size: int = test_settings.batch_size) -> list[tuple]:
    data = [
        (
            str(uuid4()),
            datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S.%f"),
            str(uuid4()),
            random.choice((480, 720, 1080, 2160)),
            random.choice((480, 720, 1080, 2160)),
        )
        for _ in range(batch_size)
    ]
    return data


def join_values(batch: list[tuple]) -> str:
    return ", ".join(
        [
            f"('{event[0]}', '{event[1]}', '{event[2]}', {event[3]}, {event[4]})"
            for event in batch
        ]
    )
