from typing import Optional, Any
from pydantic import BaseModel
from firebase_admin.firestore import firestore


class Conversation(BaseModel):
    id: Optional[str] = None
    type: str
    message: str
    created_at: Optional[Any] = firestore.SERVER_TIMESTAMP
    updated_at: Optional[Any] = firestore.SERVER_TIMESTAMP


class AddConversation(BaseModel):
    type: str
    message: str


class SetConversation(BaseModel):
    id: str
    type: str
    message: str
