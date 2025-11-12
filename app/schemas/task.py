from pydantic import BaseModel, ConfigDict, Field
from typing import Annotated
from datetime import date

class TaskBase(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=100)]
    description: Annotated[str | None, Field(None, max_length=500)] = None
    deadline: Annotated[date | None, Field(None)] = None
    status: Annotated[bool, Field(False)] = False

class PutTasksRequest(TaskBase):
    task_id: Annotated[int, Field(gt=0)]

class PostTaskRequest(TaskBase):
    user_id: Annotated[int, Field(gt=0)]

class TaskResponse(TaskBase):
    task_id: Annotated[int, Field(alias="id")]
    user_id: Annotated[int, Field(gt=0)]

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "task_id": 1,
                "user_id": 1,
                "name": "Example Task",
                "description": "Example task description.",
                "deadline": "2024-12-31",
                "status": True
            }
        }
    )
