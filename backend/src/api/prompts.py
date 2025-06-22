"""Prompts API routes."""

from typing import Optional
from fastapi import APIRouter
from pydantic import BaseModel
from ..agent import ask_deck_advice


class PromptRequest(BaseModel):
    player_id: Optional[str] = None
    message: str


router = APIRouter()


@router.post("/")
async def prompts(request: PromptRequest):
    response = ask_deck_advice(
        user_input=request.message,
        player_id=request.player_id,
    )
    if hasattr(response, "output_text"):
        return {"message": response.output_text}
    return {"message": "No output text found in response."}
