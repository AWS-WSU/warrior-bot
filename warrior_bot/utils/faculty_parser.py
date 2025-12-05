"""
Utility for parsing faculty names from the Wayne State University bulletin.

This module extracts, cleans, and structures faculty names from the
bulletins.wayne.edu/faculty/ page into a JSON cache file.
"""

import json
import os
from dataclasses import asdict, dataclass
from urllib.request import urlopen

import appdirs
from bs4 import BeautifulSoup

BULLETIN_URL = "https://bulletins.wayne.edu/faculty/"
CACHE_FILE = "faculty_cache.json"


@dataclass
class FacultyName:
    """Structured representation of a faculty member's name."""

    first: str
    middle: str | None
    last: str

    def __str__(self) -> str:
        if self.middle:
            return f"{self.first} {self.middle} {self.last}"
        return f"{self.first} {self.last}"


def fetch_bulletin_html() -> str:
    """Fetch the raw HTML from the Wayne State bulletin faculty page.

    Returns:
        The decoded HTML content of the bulletin faculty page.
    """
    response = urlopen(BULLETIN_URL)
    html: str = response.read().decode("utf-8")
    return html


def parse_raw_names(html: str) -> list[str]:
    """Extract raw name strings from the bulletin HTML.

    Args:
        html: The HTML content of the bulletin page.

    Returns:
        List of raw name strings in "LAST, FIRST MIDDLE" format.
    """
    soup = BeautifulSoup(html, features="html.parser")

    for tag in soup(["script", "style"]):
        tag.extract()

    raw_names: list[str] = []
    for p in soup.find_all("p"):
        text = p.get_text(strip=True)
        if ":" in text and len(text) > 0 and text[0].isupper():
            name_part = text.split(":")[0].strip()
            if "," in name_part:
                raw_names.append(name_part)

    return raw_names


def clean_name(raw_name: str) -> FacultyName | None:
    """Parse and clean a raw name string into structured components.

    Handles formats like:
        - "SMITH, JOHN" -> first="John", middle=None, last="Smith"
        - "SMITH, JOHN A." -> first="John", middle="A.", last="Smith"
        - "SMITH, JOHN ADAM" -> first="John", middle="Adam", last="Smith"
        - "O'BRIEN, MARY" -> first="Mary", middle=None, last="O'Brien"

    Args:
        raw_name: Name string in "LAST, FIRST [MIDDLE]" format.

    Returns:
        FacultyName with parsed components, or None if parsing fails.
    """
    parts = [p.strip() for p in raw_name.split(",", 1)]
    if len(parts) < 2:
        return None

    last_raw = parts[0].strip()
    first_parts = parts[1].strip().split()

    if not first_parts:
        return None

    def title_case(s: str) -> str:
        """Convert to title case, preserving apostrophes and hyphens."""
        result: list[str] = []
        for part in s.split("-"):
            if "'" in part:
                subparts = part.split("'")
                part = "'".join(p.capitalize() for p in subparts)
            else:
                part = part.capitalize()
            result.append(part)
        return "-".join(result)

    last = title_case(last_raw)
    first = title_case(first_parts[0])

    middle: str | None = None
    if len(first_parts) > 1:
        middle_parts = first_parts[1:]
        middle = " ".join(title_case(p) for p in middle_parts)

    return FacultyName(first=first, middle=middle, last=last)


def build_faculty_cache(output_path: str | None = None) -> list[dict[str, str | None]]:
    """Fetch, parse, and save faculty names to a JSON cache.

    Args:
        output_path: Path to write the JSON file. If None, writes to
            warrior_bot/data/faculty_cache.json.

    Returns:
        List of faculty name dictionaries that were saved.
    """
    if output_path is None:
        output_path = get_cache_path()

    html = fetch_bulletin_html()
    raw_names = parse_raw_names(html)

    seen: set[str] = set()
    faculty: list[dict[str, str | None]] = []

    for raw_name in raw_names:
        parsed = clean_name(raw_name)
        if parsed:
            key = f"{parsed.first}|{parsed.middle}|{parsed.last}".lower()
            if key not in seen:
                seen.add(key)
                faculty.append(asdict(parsed))

    with open(output_path, "w") as f:
        json.dump(faculty, f, indent=2)

    return faculty


def get_cache_path() -> str:
    """Get the default cache path for the faculty cache JSON file.

    Returns:
        The path to the faculty cache JSON file.
    """
    cache_dir: str = appdirs.user_cache_dir("warrior_bot", "warrior_bot")
    os.makedirs(cache_dir, exist_ok=True)
    return os.path.join(cache_dir, "faculty_cache.json")


def load_faculty_cache(cache_path: str | None = None) -> list[dict[str, str | None]]:
    """Load faculty names from the JSON cache.

    Args:
        cache_path: Path to the JSON file. If None, reads from
            warrior_bot/data/faculty_cache.json.

    Returns:
        List of faculty name dictionaries.
    """
    if cache_path is None:
        cache_path = get_cache_path()

    if not os.path.exists(cache_path):
        package_path = os.path.join(os.path.dirname(__file__), "..", "data", CACHE_FILE)
        if os.path.exists(package_path):
            import shutil

            shutil.copy(package_path, cache_path)
            return load_faculty_cache(cache_path)
        return []

    try:
        with open(cache_path, "r") as f:
            data: list[dict[str, str | None]] = json.load(f)
            return data
    except (json.JSONDecodeError, IOError):
        return []


if __name__ == "__main__":
    print("Building faculty cache from bulletin...")
    results = build_faculty_cache()
    print(f"Saved {len(results)} faculty names to cache.")
