from fastapi import FastAPI
from .api import decks_api, players_api, prompts_api


app = FastAPI()


@app.get("/", response_model=dict)
async def read_root():
    return {"message": "Welcome to the RoyaleAPI Decks API"}


app.include_router(decks_api, prefix="/decks")
app.include_router(players_api, prefix="/players")
app.include_router(prompts_api, prefix="/prompts")
