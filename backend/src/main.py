from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import chat_api, decks_api, players_api, prompts_api


app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_model=dict)
async def read_root():
    return {"message": "Welcome to the RoyaleAPI Decks API"}


app.include_router(chat_api, prefix="/chat")
app.include_router(decks_api, prefix="/decks")
app.include_router(players_api, prefix="/players")
app.include_router(prompts_api, prefix="/prompts")
