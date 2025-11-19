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
from typing import Generator
from urllib.request import urlopen

from bs4 import BeautifulSoup


class StaffExtractor:
    DIR_URL = "https://wayne.edu/people?type=people&q="  # Directory search URL
    STAFF_URL = "https://wayne.edu/people/"  # Base URL for staff profiles

    def __init__(self) -> None:
        pass

    def _fetch_soup_dir(self, query: str) -> BeautifulSoup:
        """Fetch and parse the HTML content from the staff directory search page.

        Args:
            query (str): The search query for the staff member.

        """
        url: str = f"{self.DIR_URL}{query.replace(' ', '+')}"
        html: str = urlopen(url).read()
        soup: BeautifulSoup = BeautifulSoup(html, features="html.parser")

        # Kill all script and style elements
        for tag in soup(["script", "style"]):
            tag.extract()

        return soup

    def _fetch_soup_staff(self, query: str) -> BeautifulSoup:
        """Fetch and parse the HTML content from the staff directory search page.

        Args:
            query (str): The search query for the staff member.

        """
        url: str = f"{self.STAFF_URL}{query.replace(' ', '+')}"
        html: str = urlopen(url).read()
        soup: BeautifulSoup = BeautifulSoup(html, features="html.parser")

        # Kill all script and style elements
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
        parts = [p for p in name.strip().split() if p]
        return " ".join(part.capitalize() for part in parts)

    def resolve_name_to_id(self, name: str) -> str | None:
        """
        Args:
            name (str): The full name of the staff member to look up.
        """
        soup: BeautifulSoup = self._fetch_soup_dir(name)
        tokens = set(name.lower().replace(",", "").split())

        for a in soup.find_all("a", href=True):
            href = str(a["href"])

            if href.startswith("/people/"):

                text = a.get_text(strip=True).lower().replace(",", "")
                words = set(text.split())

                if tokens.issubset(words):
                    staff_id = href.strip("/").split("/")[-1]
                    return staff_id

        return None

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
