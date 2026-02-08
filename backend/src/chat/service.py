from sqlmodel import Session, select
from typing import Optional, List
from .models import Conversation, Message, ConversationWithMessages, MessageRead
from uuid import UUID
from datetime import datetime
import json


class ChatService:
    def __init__(self, session: Session):
        self.session = session

    def get_or_create_conversation(self, user_id: str, conversation_id: Optional[str] = None) -> Conversation:
        """Get existing conversation or create a new one"""
        if conversation_id:
            # Try to get existing conversation
            statement = select(Conversation).where(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id
            )
            conversation = self.session.exec(statement).first()
            if conversation:
                return conversation

        # Create new conversation
        conversation = Conversation(user_id=user_id)
        self.session.add(conversation)
        self.session.commit()
        self.session.refresh(conversation)
        return conversation

    def add_message(self, conversation_id: str, user_id: str, role: str, content: str) -> Message:
        """Add a message to a conversation"""
        message = Message(
            conversation_id=conversation_id,
            user_id=user_id,
            role=role,
            content=content
        )
        self.session.add(message)
        self.session.commit()
        self.session.refresh(message)
        return message

    def get_conversation_with_messages(self, conversation_id: str, user_id: str) -> Optional[ConversationWithMessages]:
        """Get conversation with all its messages"""
        statement = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
        conversation = self.session.exec(statement).first()

        if not conversation:
            return None

        # Get messages for this conversation
        message_statement = select(Message).where(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at)
        messages = self.session.exec(message_statement).all()

        return ConversationWithMessages(
            id=conversation.id,
            user_id=conversation.user_id,
            created_at=conversation.created_at,
            updated_at=conversation.updated_at,
            messages=[MessageRead(
                id=msg.id,
                conversation_id=msg.conversation_id,
                user_id=msg.user_id,
                role=msg.role,
                content=msg.content,
                created_at=msg.created_at
            ) for msg in messages]
        )

    def get_recent_messages(self, conversation_id: str, limit: int = 10) -> List[Message]:
        """Get recent messages from a conversation"""
        statement = select(Message).where(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at.desc()).limit(limit)
        messages = self.session.exec(statement).all()
        return list(reversed(messages))  # Return in chronological order