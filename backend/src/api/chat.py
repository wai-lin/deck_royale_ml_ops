from fastapi import APIRouter
from pydantic import BaseModel
from ..agent import ask_agent, AgentResponseJSON
from ..clashroyale import get_card_by_name
from ..db import ChatManager, chat_schemas

router = APIRouter()


class PromptRequest(BaseModel):
    player_id: str
    conversation_id: str
    message: str


@router.post("/")
def chat(req: PromptRequest):
    """Handle a chat request."""
    try:
        agent_resp = ask_agent(
            player_id=req.player_id,
            user_input=req.message,
        )
        if not agent_resp:
            return {"error": "No response from agent."}
        
        output = agent_resp["output"].copy()

        try:
            full_cards = []
            for card_name in output.cards:
                card = get_card_by_name(card_name)
                if not card:
                    return {"error": f"Card '{card_name}' not found."}
                full_cards.append(card)
            output.cards = full_cards
        except Exception as e:
            return {"error": f"Error retrieving cards: {str(e)}"}
        
        try:
            chat_manager = ChatManager(player_id=req.player_id)
            chat_manager.add_message(
                req.conversation_id,
                chat_schemas.Message(
                    role="user",
                    content=req.message,
                ).model_dump()
            )
            chat_manager.add_message(
                req.conversation_id,
                chat_schemas.Message(
                    role="assistant",
                    content=output.model_dump(),
                    assistant_response_id=agent_resp["id"],
                ).model_dump()
            )
        except Exception as e:
            return {"error": f"Error saving chat messages: {str(e)}"}

        return {
            "response": output.model_dump(),
            "agent_response_id": agent_resp["id"],
        }
    except Exception as e:
        return {"error": str(e)}
