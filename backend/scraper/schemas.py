from typing import List, Optional
from pydantic import BaseModel, HttpUrl


class PartnerVideo(BaseModel):
    partner_name: Optional[str]
    video_title: Optional[str]
    video_url: Optional[HttpUrl]
    thumbnail_url: Optional[HttpUrl]


class Card(BaseModel):
    name: str
    key: str
    image_url: Optional[HttpUrl]


class DeckStats(BaseModel):
    rating: Optional[str] = None
    usage: Optional[str] = None
    wins: Optional[str] = None
    draws: Optional[str] = None
    losses: Optional[str] = None


class TopPlayer(BaseModel):
    name: Optional[str]
    trophies: Optional[str]


class Deck(BaseModel):
    deck_id: str
    card_keys: List[str]
    deck_name_mobile: Optional[str]
    deck_name_desktop: Optional[str]
    cards: List[Card]
    stats: List[DeckStats]
    avg_elixir: Optional[float]
    four_cards_cycle: Optional[float]
    deck_stats_url: Optional[str]
    copy_deck_url: Optional[HttpUrl]
    qrcode_data: Optional[str]
    top_player: Optional[TopPlayer]
    partner_videos: List[PartnerVideo] = []
