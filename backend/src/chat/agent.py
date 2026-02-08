from typing import Dict, Any, List, Optional
from .models import Message
from .service import ChatService
from .openai_agent import OpenAIAgent
from sqlmodel import Session
import asyncio


class TodoAgent:
    """
    Todo Management AI Agent that follows the specification:
    - Role: Todo Management AI Agent
    - Tools: MCP tools for managing tasks (via OpenAI Agent)
    - Behaviors: add, list, complete, delete, update tasks
    - Memory: Stateless. Conversation comes from DB.
    """

    def __init__(self, db_session: Session):
        self.chat_service = ChatService(db_session)
        self.openai_agent = OpenAIAgent(db_session)  # Use the OpenAI agent for processing

    async def process_message(self, user_id: str, conversation_id: Optional[str], message_content: str) -> Dict[str, Any]:
        """
        Process a user message following the specified flow:
        1. Fetch conversation history
        2. Store user message
        3. Run agent
        4. Capture MCP tool calls
        5. Store assistant response
        6. Return response
        """
        try:
            # 1. Fetch conversation history (get or create conversation)
            conversation = self.chat_service.get_or_create_conversation(user_id, conversation_id)

            # 2. Store user message
            user_message = self.chat_service.add_message(
                conversation_id=conversation.id,
                user_id=user_id,
                role="user",
                content=message_content
            )

            # 3. Run agent - directly await the async function
            agent_result = await self.openai_agent.process_request(user_id, message_content, self.chat_service.session)

            response_content = agent_result["response"]

            # 4. Capture MCP tool calls
            tool_calls = agent_result["tool_calls"]

            # 5. Store assistant response
            assistant_message = self.chat_service.add_message(
                conversation_id=conversation.id,
                user_id=user_id,
                role="assistant",
                content=response_content
            )

            # 6. Return response
            return {
                "conversation_id": conversation.id,
                "response": response_content,
                "tool_calls": tool_calls,
                "tool_results": agent_result.get("results", [])
            }
        except Exception as e:
            import traceback
            error_traceback = traceback.format_exc()
            print(f"Error in process_message: {str(e)}")
            print(f"Traceback: {error_traceback}")
            raise