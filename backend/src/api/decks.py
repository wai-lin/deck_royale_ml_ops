"""Decks API routes."""

from typing import List
from pydantic import BaseModel
from fastapi import HTTPException, APIRouter
from ..meta_decks import decks
from ..meta_decks.schemas import Deck


class DeckListResponse(BaseModel):
    total: int
    decks: List[Deck]


router = APIRouter()


@router.get("/", response_model=DeckListResponse)
async def get_decks():
    popular_decks = decks.get_popular_decks()
    return DeckListResponse(total=len(popular_decks), decks=popular_decks)


@router.get("/{deck_id}", response_model=Deck)
async def get_deck(deck_id: str):
    for deck in decks.get_popular_decks():
        if deck.deck_id == deck_id:
            return deck
    raise HTTPException(status_code=404, detail="Deck not found")
