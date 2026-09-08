from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

tasks = [
    {"id": 1, "title": "Buy milk", "done": False},
    {"id": 2, "title": "Study Python", "done": True},
    {"id": 3, "title": "Go for a walk", "done": False}
]


class TaskCreate(BaseModel):
    title: str


@app.get("/")
def home():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/tasks")
def get_tasks():
    return tasks


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )


@app.post("/tasks", status_code=201)
def create_task(task_data: TaskCreate):
    title = task_data.title

    if not title.strip():
        raise HTTPException(
            status_code=400,
            detail="Title is required"
        )

    new_id = max([task["id"] for task in tasks], default=0) + 1

    new_task = {
        "id": new_id,
        "title": title.strip(),
        "done": False
    }

    tasks.append(new_task)

    return new_task