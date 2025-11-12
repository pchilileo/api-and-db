from fastapi import Depends, APIRouter, Query
from typing import Annotated

from app.database import get_session
from app.schemas.task import *
import app.schemas.task as TaskSchema
import app.services.task_Service as task_Service

router = APIRouter()

@router.post("/",
             response_model=TaskSchema.TaskResponse,
             status_code=201)
async def create_tasks(request: TaskSchema.PostTaskRequest, 
                       session = Depends(get_session)
) -> TaskSchema.TaskResponse:
    created_task = task_Service.create_tasks(request, session)
    return TaskSchema.TaskResponse.model_validate(created_task)
    
@router.put("/",
            response_model=TaskSchema.TaskResponse,
            status_code=200)
async def update_tasks(request: TaskSchema.PutTasksRequest, session = Depends(get_session)
) -> TaskSchema.TaskResponse:
    task = task_Service.update_tasks(request, session)
    return task

@router.get("/",
            response_model=list[TaskSchema.TaskResponse] | TaskSchema.TaskResponse,
            status_code=200)
async def get_tasks(user_id: Annotated[int, Query(gt=0)], 
                    task_id: Annotated[int | None, Query(gt=0)] = None, 
                    session = Depends(get_session)
) -> list[TaskSchema.TaskResponse] | TaskSchema.TaskResponse:
    task = task_Service.get_tasks(user_id, task_id, session)
    return task
    
@router.delete("/",
               status_code=200)
async def delete_tasks(user_id: Annotated[int, Query(gt=0)], 
                       task_id: Annotated[int | None, Query(gt=0)] = None, 
                       session = Depends(get_session)
) -> None:
    task_Service.delete_tasks(user_id, task_id, session)