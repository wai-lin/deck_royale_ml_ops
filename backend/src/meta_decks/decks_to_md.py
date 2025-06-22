from .schemas import Deck


def decks_to_md(decks: list[Deck]):
    """Converts a list of Deck objects into a markdown formatted string."""

    decks_md = ""

    for deck in decks:
        d = f"- {deck.deck_id}\n"
        d += f"  - Name: {deck.deck_name_desktop}\n"
        d += f"  - Average Elixir: {deck.avg_elixir}\n"
        d += f"  - Four Cards Cycle: {deck.four_cards_cycle}\n"

        d += "  - Stats:\n"
        for stat in deck.stats:
            d += f"    - Rating: {stat.rating}\n"
            d += f"    - Usage: {stat.usage}\n"
            d += f"    - Wins: {stat.wins}\n"
            d += f"    - Draws: {stat.draws}\n"
            d += f"    - Losses: {stat.losses}\n"

        d += "  - Cards:\n"
        for card in deck.cards:
            d += f"    - {card.name} (key:{card.key}\n"

        d += "  - Top Player:\n"
        d += f"    - Name: {deck.top_player.name}\n"
        d += f"    - Trophies: {deck.top_player.trophies}\n"

        if len(deck.partner_videos) > 0:
            d += "  - YouTube Videos:\n"
            for yt_video in deck.partner_videos:
                d += f"    - Title: {yt_video.video_title}\n"
                d += f"    - YouTuber: {yt_video.partner_name}\n"
                d += f"    - URL: {yt_video.video_url}\n"
        else:
            d += "  - YouTube Videos: None\n"

        decks_md += d

    return decks_md
