from .schemas import Player


def player_to_md(player: Player):
    """Convert player information to markdown format."""

    if not player:
        return "No player information available."

    md = "___\n"
    md += "## Player Information\n"
    md += f"- **Tag**: {player.tag}\n"
    md += f"- **Name**: {player.name}\n"
    md += f"- **Trophies**: {player.trophies}\n"
    md += f"- **Wins**: {player.wins} \n"
    md += f"- **Losses**: {player.losses} \n"

    md += "- **Owned Cards**: "
    for card in player.cards:
        md += f"`{card.name} (level: {card.level})`,"
    md += "\n"

    md += "- **Owned Support Cards**: "
    for card in player.supportCards:
        md += f"`{card.name} (level: {card.level})`,"
    md += "\n"

    md += "- **Current Deck**: \n"
    md += "  - **Cards**: "
    for card in player.currentDeck:
        md += f"`{card.name} (level: {card.level})`,"
    md += "\n"
    md += "  - **Support Cards**: "
    for card in player.currentDeckSupportCards:
        md += f"`{card.name} (level: {card.level})`,"
    md += "\n"
    md += "___\n"

    return md
