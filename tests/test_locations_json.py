import json
import os
from typing import Generator

import pytest

from warrior_bot.core.data_handler import DataHandler

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "warrior_bot", "data")
DATA_FILE = os.path.join(DATA_DIR, "locations.json")


@pytest.fixture(scope="module")
def handler() -> Generator[DataHandler, None, None]:
    if not os.path.exists(DATA_FILE):
        pytest.skip("locations.json not found")
    yield DataHandler(DATA_DIR, "locations.json")


def test_json_is_valid() -> None:
    with open(DATA_FILE, "r") as f:
        data: dict[str, object] = json.load(f)
    assert isinstance(data, dict)


def test_all_entries_reachable(handler: DataHandler) -> None:
    for key, value in handler.flat.items():
        tail_parts = key.lower().split()[-2:]
        query = " ".join(tail_parts)
        result = handler.search(query)
        assert result == value, f"Query '{query}' failed for key '{key}'"


@pytest.mark.parametrize(
    ("query", "expected_substring"),
    [
        ("panda express", "Student Center"),
        ("taco bell", "Student Center"),
        ("UGL", "Library"),
        ("fitness center", "pool"),
    ],
)
def test_manual_known_queries(
    handler: DataHandler, query: str, expected_substring: str
) -> None:
    result = handler.search(query)
    assert result and expected_substring.lower() in result.lower()
