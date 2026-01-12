from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.sql import func
import uuid
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(nullable=False, max_length=500)
    description: Optional[str] = Field(default=None)
    is_completed: bool = Field(default=False)
    due_date: Optional[datetime] = Field(default=None)
    priority: str = Field(default="medium", max_length=20)  # low, medium, high
    created_at: datetime = Field(sa_column=Column(DateTime, default=func.now(), nullable=False))
    updated_at: datetime = Field(sa_column=Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False))
    user_id: uuid.UUID = Field(
        sa_column=Column(PG_UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    )


class TaskCreate(SQLModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: str = "medium"  # low, medium, high


class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None
    due_date: Optional[datetime] = None
    priority: Optional[str] = None  # low, medium, high


class TaskPublic(SQLModel):
    id: uuid.UUID
    title: str
    description: Optional[str] = None
    is_completed: bool
    due_date: Optional[datetime] = None
    priority: str
    created_at: datetime
    updated_at: datetime
    user_id: uuid.UUID