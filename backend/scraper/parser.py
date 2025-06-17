from bs4 import BeautifulSoup
from .schemas import Deck, Card, DeckStats, TopPlayer, PartnerVideo


def parse_decks(soup: BeautifulSoup) -> list[Deck]:
    """
    Parses a list of deck HTML elements into a list of Deck objects.
    Args:
        decks (list): A list of BeautifulSoup elements representing decks.
    Returns:
        list[Deck]: A list of Deck objects parsed from the HTML elements.
    """
    decks = soup.select("div[id^='deck_'][id$='_container']")
    parsed_decks: list[Deck] = []

    for deck_div in decks:
        check_deck_name = deck_div.select_one(
            ".deck_human_name-mobile"
        ) or deck_div.select_one(".deck_human_name-desktop")
        check_cards = deck_div.select(".deck_card__four_wide img.deck_card")
        if not check_deck_name or not check_cards:
            print(
                f"Skipping deck due to missing name or cards: {deck_div.get('id', 'Unknown ID')}"
            )
            continue

        deck_id = deck_div.get("id", "")
        card_keys = deck_div.get("data-name", "").split(",")

        deck_name_mobile = None
        deck_name_desktop = None
        mobile_name_tag = deck_div.select_one(".deck_human_name-mobile")
        desktop_name_tag = deck_div.select_one(".deck_human_name-desktop")
        if mobile_name_tag:
            deck_name_mobile = mobile_name_tag.text.strip()
        if desktop_name_tag:
            deck_name_desktop = desktop_name_tag.text.strip()

        # Cards
        cards = []
        card_imgs = deck_div.select(".deck_card__four_wide img.deck_card")
        for img in card_imgs:
            cards.append(
                Card(
                    name=img.get("alt", ""),
                    key=img.get("data-card-key", ""),
                    image_url=img.get("src"),
                )
            )

        # Stats
        stats_data = []
        stats_table = deck_div.select_one(
            "div.pad0.mobile-hide table.stats.table tbody"
        )
        if stats_table:
            rows = stats_table.find_all("tr")
            if rows and len(rows) >= 1:
                for row in rows:
                    cols = row.find_all("td")
                    if len(cols) >= 5:
                        rating = cols[0].text.strip() or None
                        usage = cols[1].text.strip().replace(",", "") or None
                        wins = cols[2].text.strip() or None
                        draws = cols[3].text.strip() or None
                        losses = cols[4].text.strip() or None
                        stats_data.append(
                            {
                                "rating": rating,
                                "usage": usage,
                                "wins": wins,
                                "draws": draws,
                                "losses": losses,
                            }
                        )
        stats = [DeckStats(**data) for data in stats_data]

        # Avg elixir and 4-cards cycle
        avg_elixir = deck_div.select_one(
            'div[data-content="Avg Elixir"] .value'
        ).text.strip()
        avg_elixir = float(avg_elixir.split("\n")[-1].strip())
        four_cards_cycle = deck_div.select_one(
            'div[data-content="4-Card Cycle"] .value'
        ).text.strip()
        four_cards_cycle = float(four_cards_cycle.split("\n")[-1].strip())

        # Links
        deck_stats_link = deck_div.select_one(
            'a.ui.active.blue.item[href^="/decks/stats/"]'
        )
        deck_stats_url = deck_stats_link.get("href") if deck_stats_link else None

        copy_deck_link = deck_div.select_one(
            'a.ui.blue.icon.circular.button[href^="https://link.clashroyale.com"]'
        )
        copy_deck_url = copy_deck_link.get("href") if copy_deck_link else None

        qrcode_div = deck_div.select_one(
            "div.ui.purple.icon.circular.button[data-qrcode]"
        )
        qrcode_data = qrcode_div.get("data-qrcode") if qrcode_div else None

        # Top player
        player_link = deck_div.select_one("a.deck_search_results__highest_trophy_link")
        top_player = None
        if player_link:
            player_name_div = player_link.select_one("div.player.item")
            trophy_icon_div = player_link.select_one("div.trophy.icon")
            trophies = None
            if trophy_icon_div:
                trophy_parent_div = trophy_icon_div.parent
                trophies = trophy_parent_div.get_text(strip=True)
            top_player = TopPlayer(
                name=player_name_div.text.strip() if player_name_div else None,
                trophies=trophies,
            )

        # Partner videos parsing
        partner_videos = []
        partner_sections = deck_div.select("div.ui.equal.width.grid > div.column")
        for partner_div in partner_sections:
            partner_name_tag = partner_div.select_one("h5.ui.partner_name.header")
            partner_name = partner_name_tag.text.strip() if partner_name_tag else None

            video_link_tag = partner_div.select_one("a[data-type='content']")
            video_url = video_link_tag.get("data-url") if video_link_tag else None
            video_title = (
                video_link_tag.select_one("span.mobile-hide").text.strip()
                if video_link_tag and video_link_tag.select_one("span.mobile-hide")
                else None
            )
            thumbnail_img = video_link_tag.select_one("img") if video_link_tag else None
            thumbnail_url = thumbnail_img.get("src") if thumbnail_img else None

            if partner_name or video_url or video_title or thumbnail_url:
                partner_videos.append(
                    PartnerVideo(
                        partner_name=partner_name,
                        video_title=video_title,
                        video_url=video_url,
                        thumbnail_url=thumbnail_url,
                    )
                )

        deck = Deck(
            deck_id=deck_id,
            card_keys=card_keys,
            deck_name_mobile=deck_name_mobile,
            deck_name_desktop=deck_name_desktop,
            cards=cards,
            stats=stats,
            avg_elixir=avg_elixir,
            four_cards_cycle=four_cards_cycle,
            deck_stats_url=deck_stats_url,
            copy_deck_url=copy_deck_url,
            qrcode_data=qrcode_data,
            top_player=top_player,
            partner_videos=partner_videos,
        )

        parsed_decks.append(deck)

    return parsed_decks
