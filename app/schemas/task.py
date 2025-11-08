from pydantic import BaseModel
from typing import Optional

class DeleteTasksRequest(BaseModel):
    task_id: Optional[int] = None
    user_id: Optional[int] = None

class PutTasksRequest(BaseModel):
    task_id: Optional[int]
    name: Optional[str] = None
    description: Optional[str] = None
    deadline: Optional[str] = None
    status: Optional[bool] = None

class PostTaskRequest(BaseModel):
    user_id: Optional[int]
    name: Optional[str]
    description: Optional[str] = None
    deadline: Optional[str] = None
    status: Optional[bool] = False