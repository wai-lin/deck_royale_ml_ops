from .scraper import Scraper

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
    )
    soup = s.scrape()

    # Extract popular decks from the BeautifulSoup object
    popular_decks = []
    decks = soup.select("div[id^='deck_']")
    # print decks as html string
    print(str(decks))

    return popular_decks
