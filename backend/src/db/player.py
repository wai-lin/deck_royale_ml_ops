from firebase_admin.firestore import firestore
from .db_init import db
from .schemas import Conversation, AddConversation, SetConversation


class Player:
    def __init__(self, id: str):
        self.player_id = id
        self.player_ref = db.collection("players").document(id)

    def add_conversation(self, conversation: AddConversation):
        """Adds a conversation for a player in the Firestore database."""
        now = firestore.SERVER_TIMESTAMP
        data = Conversation(
            type=conversation.type,
            message=conversation.message,
            created_at=now,
            updated_at=now,
        ).model_dump()

        conversations_ref = self.player_ref.collection("conversations")
        conversations_ref.add(data)

    def set_conversation(self, conversation: SetConversation):
        """Set a conversation for a player in the Firestore database."""
        now = firestore.SERVER_TIMESTAMP
        data = Conversation(
            id=conversation.id,
            type=conversation.type,
            message=conversation.message,
            created_at=now,
            updated_at=now,
        ).model_dump()

        conversations_ref = self.player_ref.collection("conversations")
        conversation_ref = conversations_ref.document(conversation.id)
        conversation_ref.set(data)
