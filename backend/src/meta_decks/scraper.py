import os
import requests
from bs4 import BeautifulSoup

CACHE_FOLDER = "cached_scrapings"


class Scraper:
    """
    A class to scrape HTML content from a given URL and cache it.
    """

    def __init__(self, url: str, cached_file_name: str, debug: bool = False):
        self.url = url
        self.cached_file_path = f"{CACHE_FOLDER}/{cached_file_name}.txt"
        self.debug = debug
        self._create_cache_file_if_not_exists()

    def _create_cache_file_if_not_exists(self):
        if not os.path.exists(CACHE_FOLDER):
            os.makedirs(CACHE_FOLDER)
        try:
            # Just check if the file can be read, not for content yet
            with open(self.cached_file_path, "r", encoding="utf-8", errors="replace") as f:
                _ = f.read()
        except FileNotFoundError:
            with open(self.cached_file_path, "w", encoding="utf-8") as f:
                f.write("")

    def _get_html(self):
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/114.0.0.0 Safari/537.36"
            )
        }
        response = requests.get(self.url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch data from {self.url}")

        return response.content.decode("utf-8")

    def scrape(self) -> BeautifulSoup:
        # Read cache if it exists
        cached_file = ""
        has_cache = False

        try:
            with open(self.cached_file_path, "r", encoding="utf-8", errors="replace") as f:
                cached_file = f.read().strip()
                has_cache = bool(cached_file)
        except FileNotFoundError:
            has_cache = False

        # If no valid cache, fetch and save new HTML
        if not has_cache:
            cached_file = self._get_html()
            with open(self.cached_file_path, "w", encoding="utf-8") as file:
                file.write(cached_file)

        if self.debug:
            print("Scraper Debug Info:")
            print("========================================")
            print(f"URL: {self.url}")
            print(f"Cache file used: {has_cache}")
            print(f"Path: {self.cached_file_path}")
            print(f"Content preview: {cached_file[:100]}")
            print("========================================")

        return BeautifulSoup(cached_file, "html.parser")
