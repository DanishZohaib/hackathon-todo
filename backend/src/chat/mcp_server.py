from typing import Dict, Any, List, Optional
from sqlmodel import Session, select
from ..models.task import Task
from ..models.user import User
from ..services.task_service import TaskService
from ..database.connection import get_session
import logging

logger = logging.getLogger(__name__)


class MCPServer:
    """
    MCP Server that implements the official MCP SDK to connect with AI agents
    This server exposes the todo management tools as MCP resources

    Rules:
    - Stateless: No state stored in memory, everything comes from DB
    - Use SQLModel for all database operations
    - Validate user_id ownership for all operations
    - Return structured responses
    """

    def __init__(self, db_session: Session):
        self.db_session = db_session
        # TaskService only has static methods, so no instantiation needed
        # The methods will receive the session as a parameter when called

    async def initialize(self):
        """Initialize the MCP server"""
        logger.info("MCP Server initialized")

    async def shutdown(self):
        """Shutdown the MCP server"""
        logger.info("MCP Server shutting down")

    async def call_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle tool calls from the AI agent
        """
        try:
            # Validate user_id ownership for all operations
            user_id = parameters.get('user_id')
            if not user_id:
                return {
                    "error": "user_id is required for all operations",
                    "success": False
                }

            # Verify user exists
            user_exists = await self._validate_user_ownership(user_id)
            if not user_exists:
                return {
                    "error": f"User {user_id} not found or unauthorized",
                    "success": False
                }

            if tool_name == "add_task":
                return await self._handle_add_task(parameters)
            elif tool_name == "list_tasks":
                return await self._handle_list_tasks(parameters)
            elif tool_name == "complete_task":
                return await self._handle_complete_task(parameters)
            elif tool_name == "delete_task":
                return await self._handle_delete_task(parameters)
            elif tool_name == "update_task":
                return await self._handle_update_task(parameters)
            else:
                return {
                    "error": f"Unknown tool: {tool_name}",
                    "success": False
                }
        except Exception as e:
            logger.error(f"MCP server error: {str(e)}")
            return {
                "error": str(e),
                "success": False
            }

    async def _validate_user_ownership(self, user_id: str) -> bool:
        """Validate that the user exists in the database"""
        try:
            # Convert user_id to proper UUID format for comparison with database
            normalized_user_id = self._normalize_user_id_for_query(user_id)
            statement = select(User).where(User.id == normalized_user_id)
            user = self.db_session.exec(statement).first()
            return user is not None
        except Exception:
            return False

    def _normalize_user_id_for_query(self, user_id: str) -> str:
        """
        Normalize a user ID string for database queries.
        If the input is a 32-character hex string without hyphens, convert it to standard UUID format.
        Otherwise, return as is.
        """
        if len(user_id) == 32 and all(c in '0123456789abcdefABCDEF' for c in user_id):
            # Convert to lowercase and reconstruct to standard UUID format: 8-4-4-4-12
            uuid_lower = user_id.lower()
            return f"{uuid_lower[:8]}-{uuid_lower[8:12]}-{uuid_lower[12:16]}-{uuid_lower[16:20]}-{uuid_lower[20:]}"
        return user_id

    async def _handle_add_task(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle add_task tool call with user validation"""
        user_id = params.get('user_id')
        title = params.get('title')
        description = params.get('description', '')

        if not user_id or not title:
            return {
                "error": "user_id and title are required",
                "success": False
            }

        try:
            # Validate that user exists first
            user_exists = await self._validate_user_ownership(user_id)
            if not user_exists:
                return {
                    "error": f"User {user_id} not found or unauthorized",
                    "success": False
                }

            # Normalize user_id for proper UUID format in database
            normalized_user_id = self._normalize_user_id_for_query(user_id)

            import uuid
            
            # Create new task with proper UUID format
            # Convert the normalized user_id string to a UUID object if it's not already
            user_uuid = normalized_user_id if isinstance(normalized_user_id, uuid.UUID) else uuid.UUID(normalized_user_id)
            new_task = Task(
                title=title,
                description=description,
                user_id=user_uuid,  # Use the UUID object
                is_completed=False  # Use the correct field name from the Task model
            )

            self.db_session.add(new_task)
            self.db_session.commit()
            self.db_session.refresh(new_task)

            # Return structured response
            result = {
                "id": str(new_task.id),
                "user_id": new_task.user_id,
                "title": new_task.title,
                "description": new_task.description,
                "is_completed": new_task.is_completed,
                "created_at": new_task.created_at.isoformat() if new_task.created_at else None
            }

            return {
                "result": result,
                "success": True
            }
        except Exception as e:
            logger.error(f"Error adding task: {str(e)}")
            import traceback
            logger.error(f"Full traceback: {traceback.format_exc()}")
            return {
                "error": f"Failed to add task: {str(e)}",
                "success": False
            }

    async def _handle_list_tasks(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle list_tasks tool call with user validation"""
        user_id = params.get('user_id')
        status = params.get('status')  # Optional status filter

        if not user_id:
            return {
                "error": "user_id is required",
                "success": False
            }

        try:
            # Validate that user exists first
            user_exists = await self._validate_user_ownership(user_id)
            if not user_exists:
                return {
                    "error": f"User {user_id} not found or unauthorized",
                    "success": False
                }

            import uuid
            
            # Build query based on filters - normalize user_id for proper UUID comparison
            normalized_user_id = self._normalize_user_id_for_query(user_id)
            # Convert the normalized user_id string to a UUID object if it's not already
            user_uuid = normalized_user_id if isinstance(normalized_user_id, uuid.UUID) else uuid.UUID(normalized_user_id)
            query = select(Task).where(Task.user_id == user_uuid)
            if status:
                # Map status to the correct field in the Task model
                if status == "completed":
                    query = query.where(Task.is_completed == True)
                elif status == "pending":
                    query = query.where(Task.is_completed == False)

            tasks = self.db_session.exec(query.order_by(Task.created_at)).all()

            # Return structured response
            result = {
                "tasks": [
                    {
                        "id": str(task.id),
                        "user_id": task.user_id,
                        "title": task.title,
                        "description": task.description,
                        "is_completed": task.is_completed,
                        "created_at": task.created_at.isoformat() if task.created_at else None,
                        "updated_at": task.updated_at.isoformat() if task.updated_at else None
                    } for task in tasks
                ],
                "total_count": len(tasks),
                "filters_applied": {"status": status} if status else {}
            }

            return {
                "result": result,
                "success": True
            }
        except Exception as e:
            logger.error(f"Error listing tasks: {str(e)}")
            import traceback
            logger.error(f"Full traceback: {traceback.format_exc()}")
            return {
                "error": f"Failed to list tasks: {str(e)}",
                "success": False
            }

    async def _handle_complete_task(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle complete_task tool call with user validation"""
        user_id = params.get('user_id')
        task_id = params.get('task_id')
        mark_complete = params.get('mark_complete', True)  # Default to True for backward compatibility

        if not user_id or not task_id:
            return {
                "error": "user_id and task_id are required",
                "success": False
            }
        
        # Validate that task_id is not an empty string
        if not task_id or (isinstance(task_id, str) and task_id.strip() == ""):
            return {
                "error": "task_id cannot be empty",
                "success": False
            }

        try:
            # Validate that user exists first
            user_exists = await self._validate_user_ownership(user_id)
            if not user_exists:
                return {
                    "error": f"User {user_id} not found or unauthorized",
                    "success": False
                }

            import uuid
            
            # Verify task belongs to user - normalize user_id for proper UUID comparison
            normalized_user_id = self._normalize_user_id_for_query(user_id)
            # Convert the normalized user_id string to a UUID object if it's not already
            user_uuid = normalized_user_id if isinstance(normalized_user_id, uuid.UUID) else uuid.UUID(normalized_user_id)
            statement = select(Task).where(Task.id == task_id, Task.user_id == user_uuid)
            task = self.db_session.exec(statement).first()

            if not task:
                return {
                    "error": f"Task {task_id} not found or does not belong to user {user_id}",
                    "success": False
                }

            # Update task completion status based on mark_complete parameter
            task.is_completed = mark_complete
            self.db_session.add(task)
            self.db_session.commit()
            self.db_session.refresh(task)

            # Return structured response
            result = {
                "id": str(task.id),
                "user_id": task.user_id,
                "title": task.title,
                "is_completed": task.is_completed,
                "updated_at": task.updated_at.isoformat() if task.updated_at else None
            }

            return {
                "result": result,
                "success": True
            }
        except Exception as e:
            logger.error(f"Error completing task: {str(e)}")
            import traceback
            logger.error(f"Full traceback: {traceback.format_exc()}")
            return {
                "error": f"Failed to complete task: {str(e)}",
                "success": False
            }

    async def _handle_delete_task(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle delete_task tool call with user validation"""
        user_id = params.get('user_id')
        task_id = params.get('task_id')

        if not user_id or not task_id:
            return {
                "error": "user_id and task_id are required",
                "success": False
            }
        
        # Validate that task_id is not an empty string
        if not task_id or (isinstance(task_id, str) and task_id.strip() == ""):
            return {
                "error": "task_id cannot be empty",
                "success": False
            }

        try:
            # Validate that user exists first
            user_exists = await self._validate_user_ownership(user_id)
            if not user_exists:
                return {
                    "error": f"User {user_id} not found or unauthorized",
                    "success": False
                }

            import uuid
            
            # Verify task belongs to user - normalize user_id for proper UUID comparison
            normalized_user_id = self._normalize_user_id_for_query(user_id)
            # Convert the normalized user_id string to a UUID object if it's not already
            user_uuid = normalized_user_id if isinstance(normalized_user_id, uuid.UUID) else uuid.UUID(normalized_user_id)
            statement = select(Task).where(Task.id == task_id, Task.user_id == user_uuid)
            task = self.db_session.exec(statement).first()

            if not task:
                return {
                    "error": f"Task {task_id} not found or does not belong to user {user_id}",
                    "success": False
                }

            # Delete the task
            self.db_session.delete(task)
            self.db_session.commit()

            # Return structured response
            result = {
                "id": str(task.id),
                "user_id": task.user_id,
                "deleted": True,
                "deleted_at": task.updated_at.isoformat() if task.updated_at else None
            }

            return {
                "result": result,
                "success": True
            }
        except Exception as e:
            logger.error(f"Error deleting task: {str(e)}")
            import traceback
            logger.error(f"Full traceback: {traceback.format_exc()}")
            return {
                "error": f"Failed to delete task: {str(e)}",
                "success": False
            }

    async def _handle_update_task(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle update_task tool call with user validation"""
        user_id = params.get('user_id')
        task_id = params.get('task_id')
        title = params.get('title')
        description = params.get('description')

        if not user_id or not task_id:
            return {
                "error": "user_id and task_id are required",
                "success": False
            }
        
        # Validate that task_id is not an empty string
        if not task_id or (isinstance(task_id, str) and task_id.strip() == ""):
            return {
                "error": "task_id cannot be empty",
                "success": False
            }

        try:
            # Validate that user exists first
            user_exists = await self._validate_user_ownership(user_id)
            if not user_exists:
                return {
                    "error": f"User {user_id} not found or unauthorized",
                    "success": False
                }

            import uuid
            
            # Verify task belongs to user - normalize user_id for proper UUID comparison
            normalized_user_id = self._normalize_user_id_for_query(user_id)
            # Convert the normalized user_id string to a UUID object if it's not already
            user_uuid = normalized_user_id if isinstance(normalized_user_id, uuid.UUID) else uuid.UUID(normalized_user_id)
            statement = select(Task).where(Task.id == task_id, Task.user_id == user_uuid)
            task = self.db_session.exec(statement).first()

            if not task:
                return {
                    "error": f"Task {task_id} not found or does not belong to user {user_id}",
                    "success": False
                }

            # Update task fields if provided
            if title is not None:
                task.title = title
            if description is not None:
                task.description = description

            self.db_session.add(task)
            self.db_session.commit()
            self.db_session.refresh(task)

            # Return structured response
            result = {
                "id": str(task.id),
                "user_id": task.user_id,
                "title": task.title,
                "description": task.description,
                "is_completed": task.is_completed,
                "updated_at": task.updated_at.isoformat() if task.updated_at else None
            }

            return {
                "result": result,
                "success": True
            }
        except Exception as e:
            logger.error(f"Error updating task: {str(e)}")
            import traceback
            logger.error(f"Full traceback: {traceback.format_exc()}")
            return {
                "error": f"Failed to update task: {str(e)}",
                "success": False
            }

    async def get_prompts(self) -> Dict[str, Any]:
        """Return available prompts for the MCP server"""
        return {
            "prompts": [
                {
                    "name": "todo_agent_prompt",
                    "description": "Prompt for the Todo Management AI Agent",
                    "text": """You are a Todo Management AI Agent.

                    TOOLS:
                    You may ONLY manage tasks using MCP tools:
                    - add_task(user_id, title, description?) - Add a new task
                    - list_tasks(user_id, status?) - List tasks
                    - complete_task(user_id, task_id) - Complete a task
                    - delete_task(user_id, task_id) - Delete a task
                    - update_task(user_id, task_id, title?, description?) - Update a task

                    BEHAVIORS:
                    - add → add_task
                    - list → list_tasks
                    - complete → complete_task
                    - delete → delete_task
                    - update → update_task

                    MEMORY:
                    Stateless. Conversation comes from DB."""
                }
            ]
        }

    async def get_tools(self) -> Dict[str, Any]:
        """Return available tools for the MCP server"""
        return {
            "tools": [
                {
                    "name": "add_task",
                    "description": "Add a new task for the user",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The ID of the user"},
                            "title": {"type": "string", "description": "The title of the task"},
                            "description": {"type": "string", "description": "Optional description of the task"}
                        },
                        "required": ["user_id", "title"]
                    }
                },
                {
                    "name": "list_tasks",
                    "description": "List tasks for the user",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The ID of the user"},
                            "status": {"type": "string", "description": "Optional status filter (pending, completed)"}
                        },
                        "required": ["user_id"]
                    }
                },
                {
                    "name": "complete_task",
                    "description": "Complete a task for the user",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The ID of the user"},
                            "task_id": {"type": "string", "description": "The ID of the task to complete"}
                        },
                        "required": ["user_id", "task_id"]
                    }
                },
                {
                    "name": "delete_task",
                    "description": "Delete a task for the user",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The ID of the user"},
                            "task_id": {"type": "string", "description": "The ID of the task to delete"}
                        },
                        "required": ["user_id", "task_id"]
                    }
                },
                {
                    "name": "update_task",
                    "description": "Update a task for the user",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The ID of the user"},
                            "task_id": {"type": "string", "description": "The ID of the task to update"},
                            "title": {"type": "string", "description": "Optional new title"},
                            "description": {"type": "string", "description": "Optional new description"}
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            ]
        }