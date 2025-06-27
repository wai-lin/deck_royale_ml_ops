import json
from typing import Optional, List
from pydantic import BaseModel
from ..get_envs import get_envs

envs = get_envs()
SCRAPED_DIR = envs['scraped_dir']


class IconUrls(BaseModel):
    """
    Represents the URLs for card icons.
    """
    medium: str
    evolutionMedium: Optional[str] = None


class Card(BaseModel):
    """
    Represents a Clash Royale card.
    """
    name: str
    id: int
    maxLevel: int
    maxEvolutionLevel: int
    elixirCost: int
    iconUrls: IconUrls
    rarity: str


with open(f"{SCRAPED_DIR}/cards.json", "r", encoding="utf-8") as file:
    cards_json = json.load(file)
    cards: List[Card] = cards_json['items'] if 'items' in cards_json else []
    support_cards: List[Card] = cards_json['supportItems'] if 'supportItems' in cards_json else []


def get_card_by_name(name: str) -> Card | None:
    """
    Get a card by its name.
    Args:
        name (str): The name of the card.
    Returns:
        Card: The card object if found, otherwise an empty Card object.
    """

    for card in cards:
        if card['name'].lower() == name.lower():
            return card
    for card in support_cards:
        if card['name'].lower() == name.lower():
            return card
    return None
