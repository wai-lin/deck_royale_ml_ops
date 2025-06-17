from typing import List

from scraper import decks
from scraper.schemas import Deck
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


@app.get("/", response_model=dict)
async def read_root():
    return {"message": "Welcome to the RoyaleAPI Decks API"}


class DeckListResponse(BaseModel):
    total: int
    decks: List[Deck]


@app.get("/decks", response_model=DeckListResponse)
async def get_decks():
    popular_decks = decks.get_popular_decks()
    return DeckListResponse(total=len(popular_decks), decks=popular_decks)


@app.get("/decks/{deck_id}", response_model=Deck)
async def get_deck(deck_id: str):
    for deck in decks.get_popular_decks():
        if deck.deck_id == deck_id:
            return deck
    raise HTTPException(status_code=404, detail="Deck not found")
