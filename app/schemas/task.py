from pydantic import BaseModel
from typing import Optional
from datetime import date

class DeleteTasksRequest(BaseModel):
    task_id: int
    user_id: Optional[int] = None

class PutTasksRequest(BaseModel):
    task_id: int
    name: Optional[str] = None
    description: Optional[str] = None
    deadline: Optional[date] = None
    status: Optional[bool] = None

class PostTaskRequest(BaseModel):
    user_id: int
    name: str
    description: Optional[str] = None
    deadline: Optional[date] = None
    status: Optional[bool] = False
