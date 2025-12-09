from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from uuid import uuid4


def generate_id() -> str:
    return str(uuid4())


class Thought(BaseModel):
    id: str = Field(default_factory=generate_id)
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class Task(BaseModel):
    id: str = Field(default_factory=generate_id)
    title: str
    description: str = ""
    created_at: datetime = Field(default_factory=datetime.now)
    due_date: Optional[datetime] = None
    is_completed: bool = False
    thought_id: Optional[str] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class ThoughtCreate(BaseModel):
    content: str


class TaskCreate(BaseModel):
    title: str
    description: str = ""
    due_date: Optional[datetime] = None
    thought_id: Optional[str] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    is_completed: Optional[bool] = None


class ExtractTasksRequest(BaseModel):
    thought_id: str
    content: str


class ExtractTasksResponse(BaseModel):
    tasks: List[Task]
    used_ai: bool = False


class ThoughtWithTasks(BaseModel):
    thought: Thought
    extracted_tasks: List[Task]
    used_ai: bool = False
