from .schemas import AddConversation, SetConversation, Conversation
from .player import Player


class Schemas:
    Conversation = Conversation
    AddConversation = AddConversation
    SetConversation = SetConversation


schemas = Schemas()

__all__ = [
    "schemas",
    "Player",
]
