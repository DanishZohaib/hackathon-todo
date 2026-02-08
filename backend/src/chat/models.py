from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid


class Conversation(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ConversationRead(SQLModel):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime


class Message(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    conversation_id: str = Field(foreign_key="conversation.id", index=True)
    user_id: str = Field(index=True)
    role: str = Field(regex="^(user|assistant)$")  # Constrained to 'user' or 'assistant'
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class MessageRead(SQLModel):
    id: str
    conversation_id: str
    user_id: str
    role: str
    content: str
    created_at: datetime


class ConversationWithMessages(ConversationRead):
    messages: List[MessageRead] = []