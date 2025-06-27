from firebase_admin.firestore import firestore
from pydantic import BaseModel
from typing import Any, Optional
from .db_init import db

class Conversation(BaseModel):
    """Model for a conversation in the chat system."""
    title: str
    created_at: Any
    updated_at: Any


class Message(BaseModel):
    """Model for a message in a conversation."""
    role: str
    content: Any
    evaluation: Optional[Any] = None
    created_at: Optional[Any] = None
    updated_at: Optional[Any] = None
    assistant_response_id: Optional[str] = None


class ChatManager:
    transaction = db.transaction()

    def __init__(self, player_id: str):
        self.player_id = player_id
        self.user_ref = db.collection("users").document(player_id)
        self.convers_ref = self.user_ref.collection("conversations")

    # #region: conversation
    # def add_conversation(self, conversation_data: dict):
    #     """Add a new conversation for the player."""
    #     conversation_data.setdefault('created_at', firestore.SERVER_TIMESTAMP)
    #     conversation_data.setdefault('updated_at', firestore.SERVER_TIMESTAMP)
    #     self.convers_ref.add(conversation_data)

    # def update_conversation(self, conversation_id: str, conversation_data: dict):
    #     """Update an existing conversation by ID."""
    #     conversation_data.setdefault('updated_at', firestore.SERVER_TIMESTAMP)
    #     conv_ref = self.convers_ref.document(conversation_id)
    #     conv_ref.set(conversation_data, merge=True)
    # #endregion
    
    #region: messages
    def add_message(self, conversation_id: str, message_data: dict):
        """Add a new message to a specific conversation."""
        now = firestore.SERVER_TIMESTAMP
        message_data['created_at'] = now
        message_data['updated_at'] = now
        messages_ref = self.convers_ref.document(conversation_id).collection("messages")
        messages_ref.add(message_data)

    def update_message(self, conversation_id: str, message_id: str, message_data: dict):
        """Update an existing message in a specific conversation."""
        message_data['updated_at'] = firestore.SERVER_TIMESTAMP
        messages_ref = self.convers_ref.document(conversation_id).collection("messages")
        message_ref = messages_ref.document(message_id)
        message_ref.set(message_data, merge=True)
    #endregion
