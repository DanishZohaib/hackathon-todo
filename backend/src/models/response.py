from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid


class BaseResponse(BaseModel):
    """Base response model with common fields"""
    pass


class TokenResponse(BaseModel):
    token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: uuid.UUID
    email: str
    name: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    is_active: bool = True


class TaskResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: Optional[str] = None
    is_completed: bool = False
    due_date: Optional[datetime] = None
    priority: str = "medium"  # low, medium, high
    created_at: datetime
    updated_at: datetime
    user_id: uuid.UUID


class TaskListResponse(BaseModel):
    tasks: List[TaskResponse]
    total_count: int
    limit: int
    offset: int


class ErrorResponse(BaseModel):
    error: dict