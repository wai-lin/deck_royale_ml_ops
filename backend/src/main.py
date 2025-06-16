from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}


class Deck(BaseModel):
    deck_id: str
    name: str  # Deck name like "EvoRG FishBoy Ghost 3.3 Cycle"
    cards: List[str]  # List of card names/ids
    avg_elixir: float  # Average elixir cost
    cycle_cost: float  # 4-card cycle cost
    copy_link: str  # Clash Royale deck copy link


example_decks = [
    Deck(
        deck_id="1",
        name="EvoRG FishBoy Ghost 3.3 Cycle",
        cards=["FishBoy", "Ghost", "Ice Spirit", "Skeletons"],
        avg_elixir=3.3,
        cycle_cost=4.0,
        copy_link="https://link-to-deck.com/1",
    ),
    Deck(
        deck_id="2",
        name="Mega Minion Cycle",
        cards=["Mega Minion", "Ice Golem", "Fireball", "Zap"],
        avg_elixir=2.8,
        cycle_cost=4.0,
        copy_link="https://link-to-deck.com/2",
    ),
]


@app.get("/decks", response_model=List[Deck])
async def get_decks():
    return example_decks


@app.get("/decks/{deck_id}", response_model=Deck)
async def get_deck(deck_id: str):
    for deck in example_decks:
        if deck.deck_id == deck_id:
            return deck
    raise HTTPException(status_code=404, detail="Deck not found")
