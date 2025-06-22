from .scraper import Scraper
from .parser import parse_decks

SCRAPE_BASE_URL = "https://royaleapi.com/decks"


def get_popular_decks():
    """
    Fetches popular decks from the cached file or scrapes them if not cached.

    Returns:
        list: A list of popular decks.
    """
    s = Scraper(
        url=f"{SCRAPE_BASE_URL}/popular",
        cached_file_name="popular_decks",
        debug=True,
    ).scrape()
    return parse_decks(s)
