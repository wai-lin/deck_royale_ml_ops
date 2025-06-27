from .schemas import AddConversation, SetConversation, Conversation
from .player import Player
from .chat import ChatManager, Conversation as ChatConv, Message

class ChatSchemas:
    """Schemas for chat-related operations."""
    Conversation = ChatConv
    Message = Message

class Schemas:
    Conversation = Conversation
    AddConversation = AddConversation
    SetConversation = SetConversation


chat_schemas = ChatSchemas()
schemas = Schemas()

__all__ = [
    "chat_schemas",
    "schemas",
    "Player",
]
