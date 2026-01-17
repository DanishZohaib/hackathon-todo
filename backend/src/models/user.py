from sqlalchemy import Column, String, Boolean, DateTime, UUID
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.sql import func
import uuid
from sqlmodel import SQLModel, Field
from passlib.context import CryptContext
from typing import Optional
from datetime import datetime


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True, nullable=False, max_length=255)
    password_hash: str = Field(nullable=False)
    name: Optional[str] = Field(default=None, max_length=100)
    created_at: datetime = Field(sa_column=Column(DateTime, default=func.now(), nullable=False))
    updated_at: datetime = Field(sa_column=Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False))
    is_active: bool = Field(default=True)

    @classmethod
    def hash_password(cls, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.password_hash)


class UserCreate(SQLModel):
    email: str
    password: str = Field(min_length=1, max_length=72)
    name: Optional[str] = None


class UserUpdate(SQLModel):
    email: Optional[str] = None
    name: Optional[str] = None
    is_active: Optional[bool] = None


class UserLogin(SQLModel):
    email: str
    password: str


class UserPublic(SQLModel):
    id: uuid.UUID
    email: str
    name: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    is_active: bool