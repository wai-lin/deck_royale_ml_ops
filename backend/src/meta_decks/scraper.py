import os
import requests
from bs4 import BeautifulSoup

CACHE_FOLDER = "cached_scrapings"


class Scraper:
    """
    A class to scrape HTML content from a given URL and cache it.
    Attributes:
        url (str): The URL to scrape.
    """

    def __init__(self, url: str, cached_file_name: str, debug: bool = False):
        """
        Initializes the Scraper class.
        Ensures that the cache file exists.
        """
        self.url = url
        self.cached_file_path = f"{CACHE_FOLDER}/{cached_file_name}.txt"
        self.debug = debug
        self._create_cache_file_if_not_exists()

    def _create_cache_file_if_not_exists(self):
        if not os.path.exists(CACHE_FOLDER):
            os.makedirs(CACHE_FOLDER)
        try:
            with open(self.cached_file_path, "x") as f:
                f.write("")  # Create an empty file
        except FileExistsError:
            pass  # File already exists, no action needed

    def _get_html(self):
        """
        Fetches the HTML content of the given URL.

        Returns:
            str: The HTML content of the page.
        """
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
        """
        Scrapes the HTML content from the given URL and caches it.
        """
        # Check if the cache file exists and read its content
        has_cache = False
        cached_file = ""
        with open(self.cached_file_path, "r") as f:
            cached_file = f.read().strip()
            has_cache = cached_file != ""

        # If cache not exists, fetch the HTML content and save it to the cache file
        if not has_cache:
            cached_file = self._get_html()
            with open(self.cached_file_path, "w") as file:
                file.write(cached_file)

        # Debugging output
        if self.debug:
            print("Scraper Debug Info:")
            print("========================================")
            print(f"Scraper initialized with URL: {self.url}")
            print(f"Cache file exists: {has_cache}")
            print(f"Cache file path: {self.cached_file_path}")
            print(f"Cache file content: {cached_file[:100]}")
            print("========================================")

        return BeautifulSoup(cached_file, "html.parser")
