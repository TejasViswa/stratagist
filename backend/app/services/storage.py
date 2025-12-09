"""
Simple JSON file-based storage for thoughts and tasks.
"""
import json
import os
from datetime import datetime
from typing import List, Optional
from pathlib import Path

from ..models import Thought, Task


# Data directory
DATA_DIR = Path(__file__).parent.parent.parent / "data"
THOUGHTS_FILE = DATA_DIR / "thoughts.json"
TASKS_FILE = DATA_DIR / "tasks.json"


def ensure_data_dir():
    """Ensure data directory exists."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not THOUGHTS_FILE.exists():
        THOUGHTS_FILE.write_text("[]")
    if not TASKS_FILE.exists():
        TASKS_FILE.write_text("[]")


def datetime_serializer(obj):
    """JSON serializer for datetime objects."""
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


def parse_datetime(dt_str: Optional[str]) -> Optional[datetime]:
    """Parse datetime from ISO string."""
    if dt_str is None:
        return None
    try:
        return datetime.fromisoformat(dt_str)
    except:
        return None


# ========== THOUGHTS ==========

def get_all_thoughts() -> List[Thought]:
    """Get all thoughts."""
    ensure_data_dir()
    try:
        data = json.loads(THOUGHTS_FILE.read_text())
        return [
            Thought(
                id=t["id"],
                content=t["content"],
                timestamp=parse_datetime(t["timestamp"]) or datetime.now()
            )
            for t in data
        ]
    except:
        return []


def get_thought_by_id(thought_id: str) -> Optional[Thought]:
    """Get a thought by ID."""
    thoughts = get_all_thoughts()
    for t in thoughts:
        if t.id == thought_id:
            return t
    return None


def add_thought(thought: Thought) -> Thought:
    """Add a new thought."""
    ensure_data_dir()
    thoughts = get_all_thoughts()
    thoughts.append(thought)
    
    data = [
        {"id": t.id, "content": t.content, "timestamp": t.timestamp.isoformat()}
        for t in thoughts
    ]
    THOUGHTS_FILE.write_text(json.dumps(data, indent=2))
    return thought


def update_thought(thought_id: str, content: str) -> Optional[Thought]:
    """Update a thought's content."""
    thoughts = get_all_thoughts()
    for i, t in enumerate(thoughts):
        if t.id == thought_id:
            thoughts[i] = Thought(id=t.id, content=content, timestamp=t.timestamp)
            data = [
                {"id": th.id, "content": th.content, "timestamp": th.timestamp.isoformat()}
                for th in thoughts
            ]
            THOUGHTS_FILE.write_text(json.dumps(data, indent=2))
            return thoughts[i]
    return None


def delete_thought(thought_id: str) -> bool:
    """Delete a thought."""
    thoughts = get_all_thoughts()
    new_thoughts = [t for t in thoughts if t.id != thought_id]
    if len(new_thoughts) == len(thoughts):
        return False
    data = [
        {"id": t.id, "content": t.content, "timestamp": t.timestamp.isoformat()}
        for t in new_thoughts
    ]
    THOUGHTS_FILE.write_text(json.dumps(data, indent=2))
    return True


def get_thoughts_by_date(date: datetime) -> List[Thought]:
    """Get thoughts for a specific date."""
    thoughts = get_all_thoughts()
    return [
        t for t in thoughts
        if t.timestamp.date() == date.date()
    ]


def get_available_dates() -> List[datetime]:
    """Get all unique dates with thoughts."""
    thoughts = get_all_thoughts()
    dates = set()
    for t in thoughts:
        dates.add(datetime(t.timestamp.year, t.timestamp.month, t.timestamp.day))
    return sorted(list(dates), reverse=True)


def clear_thoughts_for_date(date: datetime) -> int:
    """Clear all thoughts for a specific date. Returns count of deleted thoughts."""
    thoughts = get_all_thoughts()
    target_date = date.date()
    new_thoughts = [t for t in thoughts if t.timestamp.date() != target_date]
    deleted_count = len(thoughts) - len(new_thoughts)
    
    data = [
        {"id": t.id, "content": t.content, "timestamp": t.timestamp.isoformat()}
        for t in new_thoughts
    ]
    THOUGHTS_FILE.write_text(json.dumps(data, indent=2))
    return deleted_count


# ========== TASKS ==========

def get_all_tasks() -> List[Task]:
    """Get all tasks."""
    ensure_data_dir()
    try:
        data = json.loads(TASKS_FILE.read_text())
        return [
            Task(
                id=t["id"],
                title=t["title"],
                description=t.get("description", ""),
                created_at=parse_datetime(t["created_at"]) or datetime.now(),
                due_date=parse_datetime(t.get("due_date")),
                is_completed=t.get("is_completed", False),
                thought_id=t.get("thought_id")
            )
            for t in data
        ]
    except:
        return []


def get_task_by_id(task_id: str) -> Optional[Task]:
    """Get a task by ID."""
    tasks = get_all_tasks()
    for t in tasks:
        if t.id == task_id:
            return t
    return None


def add_task(task: Task) -> Task:
    """Add a new task."""
    ensure_data_dir()
    tasks = get_all_tasks()
    tasks.append(task)
    _save_tasks(tasks)
    return task


def add_tasks(new_tasks: List[Task]) -> List[Task]:
    """Add multiple tasks."""
    ensure_data_dir()
    tasks = get_all_tasks()
    tasks.extend(new_tasks)
    _save_tasks(tasks)
    return new_tasks


def update_task(task_id: str, updates: dict) -> Optional[Task]:
    """Update a task."""
    tasks = get_all_tasks()
    for i, t in enumerate(tasks):
        if t.id == task_id:
            task_dict = t.model_dump()
            task_dict.update({k: v for k, v in updates.items() if v is not None})
            tasks[i] = Task(**task_dict)
            _save_tasks(tasks)
            return tasks[i]
    return None


def delete_task(task_id: str) -> bool:
    """Delete a task."""
    tasks = get_all_tasks()
    new_tasks = [t for t in tasks if t.id != task_id]
    if len(new_tasks) == len(tasks):
        return False
    _save_tasks(new_tasks)
    return True


def _save_tasks(tasks: List[Task]):
    """Save tasks to file."""
    data = [
        {
            "id": t.id,
            "title": t.title,
            "description": t.description,
            "created_at": t.created_at.isoformat(),
            "due_date": t.due_date.isoformat() if t.due_date else None,
            "is_completed": t.is_completed,
            "thought_id": t.thought_id
        }
        for t in tasks
    ]
    TASKS_FILE.write_text(json.dumps(data, indent=2))

