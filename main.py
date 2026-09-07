from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(title="Focus Flow API")

# Task Model matching app requirements
class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    priority: str  # High, Medium, Low
    energy_level: str  # Low, Medium, Deep Focus
    estimated_time: int  # minutes
    context_tag: str  # @Laptop, @Home, @Errands, @Offline
    completed: bool = False
    created_at: datetime = datetime.now()

# In-memory database for quick setup
tasks_db: List[Task] = []

@app.get("/")
def read_root():
    return {"message": "Focus Flow Python API is running!"}

# Get all tasks with smart filtering options
@app.get("/tasks", response_model=List[Task])
def get_tasks(energy: Optional[str] = None, max_time: Optional[int] = None):
    filtered_tasks = tasks_db
    if energy:
        filtered_tasks = [t for t in filtered_tasks if t.energy_level.lower() == energy.lower()]
    if max_time:
        filtered_tasks = [t for t in filtered_tasks if t.estimated_time <= max_time]
    return filtered_tasks

# Create a new task
@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    tasks_db.append(task)
    return task

# Toggle completion status
@app.patch("/tasks/{task_id}/toggle", response_model=Task)
def toggle_task(task_id: int):
    for task in tasks_db:
        if task.id == task_id:
            task.completed = not task.completed
            return task
    raise HTTPException(status_code=404, detail="Task not found")

