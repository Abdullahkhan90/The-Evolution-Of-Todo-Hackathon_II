from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from datetime import timezone
import uuid


class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True, index=True)
    password: str  # hashed password
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Relationship to tasks
    tasks: List["Task"] = Relationship(back_populates="user")


class TaskBase(SQLModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: Optional[str] = None  # high, medium, low
    tags: Optional[str] = None  # comma-separated tags
    due_date: Optional[datetime] = None
    recurrence: Optional[str] = None  # daily, weekly, monthly, etc.
    user_id: uuid.UUID = Field(foreign_key="user.id")


class Task(TaskBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Relationship to user
    user: User = Relationship(back_populates="tasks")


class Conversation(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Message(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    conversation_id: uuid.UUID = Field(foreign_key="conversation.id")
    role: str  # "user" or "assistant"
    content: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class TaskCreate(TaskBase):
    pass