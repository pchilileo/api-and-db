from fastapi import Depends, APIRouter, Request, HTTPException, Query
from pydantic import ValidationError
from typing import Annotated
import app.schemas.task as TaskSchema
from app.database import get_session
from app.schemas.task import *
import app.services.task_Service as task_Service
import json

router = APIRouter()

@router.post("/",
             openapi_extra={
                "requestBody": {
                    "content": {"application/x-json": {"schema": TaskSchema.PostTaskRequest.schema()}},
                    "required": True}})
async def create_tasks(request: Request, session = Depends(get_session)):
    raw_body = await request.body()
    try:
        data = json.loads(raw_body)
    except json.JSONDecodeError:
        raise HTTPException(status_code=422, detail="Invalid JSON")
    try:
        task = TaskSchema.PostTaskRequest.model_validate(data)
        return task_Service.create_tasks(task, session)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors(include_url=False))
    
@router.put("/",
             openapi_extra={
                "requestBody": {
                    "content": {"application/x-json": {"schema": TaskSchema.PutTasksRequest.schema()}},
                    "required": True}})
async def update_tasks(request: Request, session = Depends(get_session)):
    raw_body = await request.body()
    try:
        data = json.loads(raw_body)
    except json.JSONDecodeError:
        raise HTTPException(status_code=422, detail="Invalid JSON")
    try:
        task = TaskSchema.PutTasksRequest.model_validate(data)
        return task_Service.update_tasks(task, session)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors(include_url=False))

@router.get("/",)
async def get_tasks(user_id: int, task_id: Annotated[int | None, Query()] = None, session = Depends(get_session)):
    try:
        return task_Service.get_tasks(user_id, task_id, session)
    except:
        raise HTTPException(status_code=422, detail="Invalid parameters")
    
@router.delete("/",
             openapi_extra={
                "requestBody": {
                    "content": {"application/x-json": {"schema": TaskSchema.DeleteTasksRequest.schema()}},
                    "required": True}})
async def delete_tasks(request: Request, session = Depends(get_session)):
    raw_body = await request.body()
    try:
        data = json.loads(raw_body)
    except json.JSONDecodeError:
        raise HTTPException(status_code=422, detail="Invalid JSON")
    try:
        task = TaskSchema.DeleteTasksRequest.model_validate(data)
        return task_Service.delete_tasks(task, session)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors(include_url=False))