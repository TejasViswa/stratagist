from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from datetime import datetime

from .models import (
    Thought, ThoughtCreate, Task, TaskCreate, TaskUpdate,
    ExtractTasksRequest, ExtractTasksResponse, ThoughtWithTasks
)
from .services import storage
from .services.ai_extraction import extract_tasks_from_thought

app = FastAPI(title="StrataGist API", version="1.0.0")

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}


# ========== THOUGHTS ENDPOINTS ==========

@app.get("/api/thoughts", response_model=List[Thought])
def list_thoughts():
    """Get all thoughts, sorted by timestamp (newest first)."""
    thoughts = storage.get_all_thoughts()
    return sorted(thoughts, key=lambda t: t.timestamp, reverse=True)


@app.get("/api/thoughts/dates", response_model=List[str])
def get_thought_dates():
    """Get all unique dates that have thoughts."""
    dates = storage.get_available_dates()
    return [d.isoformat() for d in dates]


@app.get("/api/thoughts/date/{date}", response_model=List[Thought])
def get_thoughts_for_date(date: str):
    """Get thoughts for a specific date."""
    try:
        dt = datetime.fromisoformat(date)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")
    
    thoughts = storage.get_thoughts_by_date(dt)
    return sorted(thoughts, key=lambda t: t.timestamp, reverse=True)


@app.post("/api/thoughts", response_model=ThoughtWithTasks)
def create_thought(thought_create: ThoughtCreate):
    """Create a new thought and extract tasks from it."""
    thought = Thought(content=thought_create.content)
    storage.add_thought(thought)
    
    # Extract tasks from the thought
    tasks, used_ai = extract_tasks_from_thought(thought)
    
    return ThoughtWithTasks(
        thought=thought,
        extracted_tasks=tasks,
        used_ai=used_ai
    )


@app.get("/api/thoughts/{thought_id}", response_model=Thought)
def get_thought(thought_id: str):
    """Get a specific thought by ID."""
    thought = storage.get_thought_by_id(thought_id)
    if not thought:
        raise HTTPException(status_code=404, detail="Thought not found")
    return thought


@app.put("/api/thoughts/{thought_id}", response_model=Thought)
def update_thought(thought_id: str, thought_update: ThoughtCreate):
    """Update a thought's content."""
    thought = storage.update_thought(thought_id, thought_update.content)
    if not thought:
        raise HTTPException(status_code=404, detail="Thought not found")
    return thought


@app.delete("/api/thoughts/{thought_id}")
def delete_thought(thought_id: str):
    """Delete a thought."""
    if not storage.delete_thought(thought_id):
        raise HTTPException(status_code=404, detail="Thought not found")
    return {"success": True}


@app.delete("/api/thoughts/date/{date}")
def clear_thoughts_for_date(date: str):
    """Clear all thoughts for a specific date."""
    try:
        dt = datetime.fromisoformat(date)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")
    
    deleted_count = storage.clear_thoughts_for_date(dt)
    return {"success": True, "deleted_count": deleted_count}


# ========== TASKS ENDPOINTS ==========

@app.get("/api/tasks", response_model=List[Task])
def list_tasks():
    """Get all tasks, sorted by creation date (newest first)."""
    tasks = storage.get_all_tasks()
    return sorted(tasks, key=lambda t: t.created_at, reverse=True)


@app.post("/api/tasks", response_model=Task)
def create_task(task_create: TaskCreate):
    """Create a new task."""
    task = Task(
        title=task_create.title,
        description=task_create.description,
        due_date=task_create.due_date,
        thought_id=task_create.thought_id
    )
    return storage.add_task(task)


@app.post("/api/tasks/bulk", response_model=List[Task])
def create_tasks_bulk(tasks: List[TaskCreate]):
    """Create multiple tasks at once."""
    new_tasks = [
        Task(
            title=t.title,
            description=t.description,
            due_date=t.due_date,
            thought_id=t.thought_id
        )
        for t in tasks
    ]
    return storage.add_tasks(new_tasks)


@app.get("/api/tasks/{task_id}", response_model=Task)
def get_task(task_id: str):
    """Get a specific task by ID."""
    task = storage.get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.put("/api/tasks/{task_id}", response_model=Task)
def update_task(task_id: str, task_update: TaskUpdate):
    """Update a task."""
    updates = task_update.model_dump(exclude_unset=True)
    task = storage.update_task(task_id, updates)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.patch("/api/tasks/{task_id}/toggle", response_model=Task)
def toggle_task_completion(task_id: str):
    """Toggle a task's completion status."""
    task = storage.get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    updated_task = storage.update_task(task_id, {"is_completed": not task.is_completed})
    return updated_task


@app.delete("/api/tasks/{task_id}")
def delete_task(task_id: str):
    """Delete a task."""
    if not storage.delete_task(task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    return {"success": True}


# ========== EXTRACTION ENDPOINT ==========

@app.post("/api/extract-tasks", response_model=ExtractTasksResponse)
def extract_tasks(request: ExtractTasksRequest):
    """Extract tasks from text content."""
    thought = Thought(id=request.thought_id, content=request.content)
    tasks, used_ai = extract_tasks_from_thought(thought)
    return ExtractTasksResponse(tasks=tasks, used_ai=used_ai)
