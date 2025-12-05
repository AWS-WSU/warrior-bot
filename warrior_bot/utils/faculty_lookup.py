"""
Module for extracting information about a staff member of Wayne State University.

The model is explained as follows:

Attributes:
    name (str): The full name of the staff member.
    department (str): The department the staff member belongs to.
    office (str): The office location of the staff member.
    email (str): The email address of the staff member.
    phone (str): The phone number of the staff member.

Private Methods:
    _fetch_soup_dir(query: str) -> BeautifulSoup:
        Fetch and parse the HTML content from the staff directory search page.
    _fetch_soup_staff(query: str) -> BeautifulSoup:
        Fetch and parse the HTML content from the staff profile page.
    _get_raw_html(soup: BeautifulSoup) -> str:
        Extract and clean the raw text from a BeautifulSoup object.
"""

from dataclasses import dataclass
from difflib import get_close_matches
from typing import Generator
from urllib.request import urlopen

from bs4 import BeautifulSoup


class StaffLookup:
    DIR_URL = "https://wayne.edu/people?type=people&q="  # Directory search URL
    STAFF_URL = "https://wayne.edu/people/"  # Base URL for staff profiles
    MAX_PAGES = 5  # Amount of pages _fetch_soup_dir will look through.

    def __init__(self) -> None:
        pass

    def _fetch_soup_dir(self, query: str) -> BeautifulSoup:
        """Fetch and parse the HTML content from the staff directory search page.

        Args:
            query (str): The search query for the staff member.

        """
        soup: BeautifulSoup = BeautifulSoup("", features="html.parser")

        # Kill all script and style elements
        for tag in soup(["script", "style"]):
            tag.extract()

        i = 1

        while i <= self.MAX_PAGES:
            try:
                page = f"&page={i}"
                url: str = f"{self.DIR_URL}{query.replace(' ', '+')}{page}"
                html: str = urlopen(url).read()
                data: BeautifulSoup = BeautifulSoup(html, features="html.parser")

                for tag in soup(["script", "style"]):
                    tag.extract()

                soup.append(data)

                i += 1
            except Exception:
                break

        return soup

    def _fetch_soup_staff(self, query: str) -> BeautifulSoup:
        """Fetch and parse the HTML content from the staff directory search page.

        Args:
            query (str): The search query for the staff member.

        """
        url: str = f"{self.STAFF_URL}{query.replace(' ', '+')}"
        html: str = urlopen(url).read()
        soup: BeautifulSoup = BeautifulSoup(html, features="html.parser")

        for tag in soup(["script", "style"]):
            tag.extract()

        return soup

    def _get_raw_html(self, soup: BeautifulSoup) -> str:
        raw: str = soup.get_text()
        lines: Generator[str, None, None] = (line.strip() for line in raw.splitlines())
        chunks: Generator[str, None, None] = (
            phrase.strip() for line in lines for phrase in line.split("  ")
        )
        return "\n".join(chunk for chunk in chunks if chunk)

    @staticmethod
    def normalize_name(name: str) -> str:
        """Normalize name to 'First Last' format with proper capitalization."""
        parts = [p for p in name.strip().split() if p]
        if len(parts) == 2:
            parts = [parts[1], parts[0]]
        return " ".join(part.capitalize() for part in parts)

    def _build_searchable_names(self, cache: list[dict[str, str | None]]) -> list[str]:
        """Build list of searchable name strings from faculty cache.

        Creates multiple variations for each name to improve fuzzy matching:
        - "first last" (e.g., "resh mahabir")
        - "first middle last" if middle exists (e.g., "john a smith")
        - "last first" for reverse lookups (e.g., "mahabir resh")
        """
        names: list[str] = []
        for entry in cache:
            first = (entry.get("first") or "").lower()
            middle = (entry.get("middle") or "").lower()
            last = (entry.get("last") or "").lower()

            if first and last:
                names.append(f"{first} {last}")
                names.append(f"{last} {first}")
                if middle:
                    names.append(f"{first} {middle} {last}")
        return names

    def _cache_entry_to_query(self, entry: dict[str, str | None]) -> str:
        """Convert a cache entry to a search query string."""
        first = entry.get("first") or ""
        middle = entry.get("middle") or ""
        last = entry.get("last") or ""

        if middle:
            return f"{first} {middle} {last}"
        return f"{first} {last}"

    def resolve_user_input_to_name_and_id(
        self, user_input: str
    ) -> list[tuple[str, str]]:
        """Resolve user input to staff name and ID using cached faculty data.

        Fuzzy matches user input against the local faculty cache (no HTTP request),
        then queries the /people endpoint with the best match to get the staff ID.

        Args:
            user_input: The input name of the staff member to look up.

        Returns:
            List of (name, staff_id) tuples for the best match.
        """
        from warrior_bot.utils.faculty_parser import load_faculty_cache

        cache = load_faculty_cache()
        if not cache:
            return []

        query = user_input.lower().replace(",", "").strip()
        tokens = query.split()
        reversed_query = " ".join(reversed(tokens))

        searchable_names = self._build_searchable_names(cache)

        best_match: str | None = None
        for q in [query, reversed_query]:
            matches = get_close_matches(q, searchable_names, n=1, cutoff=0.6)
            if matches:
                best_match = matches[0]
                break

        if not best_match:
            return []

        match_tokens = set(best_match.split())
        corrected_query: str | None = None

        for entry in cache:
            first = (entry.get("first") or "").lower()
            last = (entry.get("last") or "").lower()

            if first in match_tokens and last in match_tokens:
                corrected_query = self._cache_entry_to_query(entry)
                break

        if not corrected_query:
            return []

        soup = self._fetch_soup_dir(corrected_query)

        for a in soup.find_all("a", href=True):
            href = str(a["href"])
            if href.startswith("/people/"):
                text = a.get_text(strip=True).lower().replace(",", "")
                staff_id = href.strip("/").split("/")[-1]
                return [(text, staff_id)]

        return []

    def resolve_id_to_department(self, staff_id: str) -> str | None:
        """
        Args:
            staff_id (str): Staff members ID.
        """

        soup: BeautifulSoup = self._fetch_soup_staff(staff_id)
        content = self._get_raw_html(soup)

        content_lines = content.splitlines()

        for line in content_lines:
            if line.startswith("Unit:"):
                return line.split("Unit:", 1)[1].strip()

        return None

    def resolve_id_to_office(self, staff_id: str) -> str | None:
        """
        Args:
            staff_id (str): Staff members ID.
        """

        soup: BeautifulSoup = self._fetch_soup_staff(staff_id)
        content = self._get_raw_html(soup)
        content_lines = content.splitlines()

        for i, line in enumerate(content_lines):
            if "Office:" in line:
                if i + 1 < len(content_lines):
                    return content_lines[i + 1]
        return None

    def resolve_id_to_email(self, staff_id: str) -> str | None:
        """
        Args:
            staff_id (str): Staff members ID.
        """

        soup: BeautifulSoup = self._fetch_soup_staff(staff_id)
        content = self._get_raw_html(soup)
        content_lines = content.splitlines()

        for i, line in enumerate(content_lines):
            if "Email:" in line:
                if i + 1 < len(content_lines):
                    return content_lines[i + 1]
        return None

    def resolve_id_to_phone(self, staff_id: str) -> str | None:
        """
        Args:
            staff_id (str): Staff members ID.
        """

        soup: BeautifulSoup = self._fetch_soup_staff(staff_id)
        content = self._get_raw_html(soup)
        content_lines = content.splitlines()

        for i, line in enumerate(content_lines):
            if "Phone:" in line:
                if i + 1 < len(content_lines):
                    return content_lines[i + 1]
        return None


@dataclass
class Staff:
    name: str | None
    department: str | None
    office: str | None
    email: str | None
    phone: str | None
