"""Players API routes."""

from fastapi import APIRouter
from ..clashroyale import get_player_info

router = APIRouter()


@router.get("/{player_id}")
async def get_player(player_id: str):
    player = get_player_info(player_id)
    return player.json()
