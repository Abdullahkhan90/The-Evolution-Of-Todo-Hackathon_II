from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid


# User schemas
class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True


# Task schemas
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: Optional[str] = None  # high, medium, low
    tags: Optional[str] = None  # comma-separated tags
    due_date: Optional[datetime] = None
    recurrence: Optional[str] = None  # daily, weekly, monthly, etc.


class TaskCreate(TaskBase):
    user_id: uuid.UUID


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None
    tags: Optional[str] = None
    due_date: Optional[datetime] = None
    recurrence: Optional[str] = None


class Task(TaskBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True