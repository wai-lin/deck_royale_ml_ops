"""Prompts API routes."""

from fastapi import APIRouter
from pydantic import BaseModel
from ..agent import ask_deck_advice
from ..db import Player, schemas


class PromptRequest(BaseModel):
    player_id: str
    message: str


router = APIRouter()


@router.post("/")
async def prompts(request: PromptRequest):
    """Handle a prompt request from a player."""

    player = Player(id=request.player_id)

    # Add a conversation entry for the prompt
    try:
        player.add_conversation(
            schemas.AddConversation(
                type="prompt",
                message=request.message,
            )
        )
    except Exception as e:
        return {"message": f"Error adding conversation: {str(e)}"}

    # Get the response from the agent
    try:
        response = ask_deck_advice(
            user_input=request.message,
            player_id=request.player_id,
        )
    except Exception as e:
        return {"message": f"Error getting response: {str(e)}"}

    # Save the response in the player's conversation
    try:
        player.set_conversation(
            schemas.SetConversation(
                id=response.id,
                type="response",
                message=response.output_text,
            )
        )
    except Exception as e:
        return {"message": f"Error setting conversation: {str(e)}"}

    # Return the response
    if hasattr(response, "id") and hasattr(response, "output_text"):
        return {"response_id": response.id, "message": response.output_text}
    return {"message": "No output text found in response."}
