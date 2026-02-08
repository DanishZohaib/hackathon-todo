from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlmodel import Session, select
from typing import Optional
from ..database.connection import get_session
from ..config import settings
from .models import Conversation, Message, ConversationWithMessages
from .agent import TodoAgent
from .service import ChatService
from pydantic import BaseModel


router = APIRouter(prefix="/api", tags=["chat"])

auth_scheme = HTTPBearer()


def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(auth_scheme),
    db_session: Session = Depends(get_session)
) -> str:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        token_type = payload.get("token_type", "access")

        # Only allow access tokens for getting current user, not refresh tokens
        if token_type != "access":
            raise HTTPException(
                status_code=401,
                detail="Access token required for this operation",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user_email: str = payload.get("sub")
        if user_email is None:
            raise HTTPException(
                status_code=401,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Find user by email to get the user ID directly using SQLModel
        from ..models.user import User
        statement = select(User).where(User.email == user_email)
        user = db_session.exec(statement).first()

        if not user:
            raise HTTPException(
                status_code=401,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return str(user.id)
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


class ChatRequest(BaseModel):
    conversation_id: Optional[str] = None
    message: str


class ChatResponse(BaseModel):
    conversation_id: str
    response: str
    tool_calls: list = []


@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat_endpoint(
    user_id: str,
    request: ChatRequest,
    current_user_id: str = Depends(get_current_user_id),
    db_session: Session = Depends(get_session)
):
    """
    Chat endpoint that processes user messages and returns AI responses
    with support for tool calls to manage todos.

    Flow:
    1. Fetch conversation history
    2. Store user message
    3. Run agent
    4. Capture MCP tool calls
    5. Store assistant response
    6. Return response

    Request:
    - conversation_id? (optional) - to continue an existing conversation
    - message (required) - the user's message

    Response:
    - conversation_id - the conversation ID (new or existing)
    - response - the AI's response
    - tool_calls[] - any tools that were called
    """
    print(f"Received chat request for user_id: {user_id}")
    print(f"Authenticated user_id: {current_user_id}")
    
    # Normalize user IDs by removing hyphens for comparison (UUID format normalization)
    normalized_user_id = user_id.replace('-', '')
    normalized_current_user_id = current_user_id.replace('-', '')

    print(f"Normalized user_id: {normalized_user_id}")
    print(f"Normalized current_user_id: {normalized_current_user_id}")

    # Validate that the user_id in the URL matches the authenticated user
    if normalized_user_id != normalized_current_user_id:
        print(f"Authorization failed: {normalized_user_id} != {normalized_current_user_id}")
        raise HTTPException(
            status_code=403,
            detail="Not authorized to access this user's chat"
        )

    # Convert normalized user ID back to proper UUID format for database operations
    # We need to reconstruct the UUID format (assuming it's a standard 32-character hex string without hyphens)
    # by adding hyphens in the correct positions: 8-4-4-4-12
    try:
        actual_user_id = _normalize_uuid_for_db(normalized_user_id)
        print(f"Actual user_id after normalization: {actual_user_id}")
    except Exception as e:
        print(f"Error normalizing UUID: {str(e)}")
        actual_user_id = user_id  # Fallback to original user_id
    
    try:
        # Initialize the agent with the database session
        agent = TodoAgent(db_session)

        # Process the message through the agent (this handles the full flow internally)
        result = await agent.process_message(
            user_id=actual_user_id,
            conversation_id=request.conversation_id,
            message_content=request.message
        )

        return ChatResponse(
            conversation_id=result["conversation_id"],
            response=result["response"],
            tool_calls=result.get("tool_calls", [])
        )
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Chat endpoint error: {str(e)}")
        print(f"Full traceback: {error_details}")
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")


def _normalize_uuid_for_db(uuid_str: str) -> str:
    """
    Normalize a UUID string for database operations.
    If the input is a 32-character hex string without hyphens, convert it to standard UUID format.
    Otherwise, return as is.
    """
    try:
        if uuid_str and len(uuid_str) == 32 and all(c in '0123456789abcdefABCDEF' for c in uuid_str):
            # Convert to lowercase and reconstruct to standard UUID format: 8-4-4-4-12
            uuid_lower = uuid_str.lower()
            return f"{uuid_lower[:8]}-{uuid_lower[8:12]}-{uuid_lower[12:16]}-{uuid_lower[16:20]}-{uuid_lower[20:]}"
        
        # If it's already in UUID format (with hyphens), validate it
        if uuid_str and len(uuid_str) == 36 and uuid_str.count('-') == 4:
            import re
            uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
            if re.match(uuid_pattern, uuid_str.lower()):
                return uuid_str
        
        return uuid_str
    except Exception as e:
        print(f"Error in _normalize_uuid_for_db: {str(e)}, input: {uuid_str}")
        return uuid_str  # Return the original string if there's an error


@router.get("/{user_id}/conversations")
async def list_user_conversations(
    user_id: str,
    current_user_id: str = Depends(get_current_user_id),
    db_session: Session = Depends(get_session)
):
    """
    Get all conversations for a user
    """
    # Normalize user IDs by removing hyphens for comparison (UUID format normalization)
    normalized_user_id = user_id.replace('-', '')
    normalized_current_user_id = current_user_id.replace('-', '')

    # Validate that the user_id in the URL matches the authenticated user
    if normalized_user_id != normalized_current_user_id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to access this user's conversations"
        )

    # Convert normalized user ID back to proper UUID format for database operations
    actual_user_id = _normalize_uuid_for_db(normalized_user_id)

    try:
        chat_service = ChatService(db_session)
        statement = select(Conversation).where(Conversation.user_id == actual_user_id).order_by(Conversation.updated_at.desc())
        conversations = db_session.exec(statement).all()
        return conversations
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching conversations: {str(e)}")


@router.get("/{user_id}/conversations/{conversation_id}")
async def get_conversation(
    user_id: str,
    conversation_id: str,
    current_user_id: str = Depends(get_current_user_id),
    db_session: Session = Depends(get_session)
):
    """
    Get a specific conversation with its messages
    """
    # Normalize user IDs by removing hyphens for comparison (UUID format normalization)
    normalized_user_id = user_id.replace('-', '')
    normalized_current_user_id = current_user_id.replace('-', '')

    # Validate that the user_id in the URL matches the authenticated user
    if normalized_user_id != normalized_current_user_id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to access this user's conversation"
        )

    # Convert normalized user ID back to proper UUID format for database operations
    actual_user_id = _normalize_uuid_for_db(normalized_user_id)

    try:
        chat_service = ChatService(db_session)
        conversation_with_messages = chat_service.get_conversation_with_messages(conversation_id, actual_user_id)

        if not conversation_with_messages:
            raise HTTPException(status_code=404, detail="Conversation not found")

        return conversation_with_messages
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching conversation: {str(e)}")


