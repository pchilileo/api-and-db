from fastapi import Depends, APIRouter, Request, HTTPException
from pydantic import ValidationError
import app.schemas.task as TaskSchema
from app.database import get_session
from app.schemas.task import *
import app.services.task_service as task_service
import yaml

router = APIRouter()

@router.post("/",
            openapi_extra={
                "requestBody": {
                    "content": {"application/x-yaml": {"schema": TaskSchema.PostTaskRequest.schema()}},
                    "required": True}})
async def create_tasks(request: Request, Session = Depends(get_session)):
    raw_body = await request.body()
    try:
        data = yaml.safe_load(raw_body)
    except yaml.YAMLError:
        raise HTTPException(status_code=422, detail="Invalid YAML")
    try:
        task = TaskSchema.PostTaskRequest.model_validate(data)
        return task_service.create_tasks(task, Session)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors(include_url=False))
    
@router.put("/",
            openapi_extra={
                "requestBody": {
                    "content": {"application/x-yaml": {"schema": TaskSchema.PutTasksRequest.schema()}},
                    "required": True}})
async def update_tasks(request: Request, Session = Depends(get_session)):
    raw_body = await request.body()
    try:
        data = yaml.safe_load(raw_body)
    except yaml.YAMLError:
        raise HTTPException(status_code=422, detail="Invalid YAML")
    try:
        task = TaskSchema.PutTasksRequest.model_validate(data)
        return task_service.update_tasks(task, Session)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors(include_url=False))

@router.post("/{user_id}/",
            openapi_extra={
                "requestBody": {
                    "content": {"application/x-yaml": {"schema": TaskSchema.GetTaskRequest.schema()}},
                    "required": True}})
async def get_tasks(request: Request, Session = Depends(get_session)):
    raw_body = await request.body()
    try:
        data = yaml.safe_load(raw_body)
    except yaml.YAMLError:
        raise HTTPException(status_code=422, detail="Invalid YAML")
    try:
        task = TaskSchema.GetTaskRequest.model_validate(data)
        return task_service.get_tasks(task, Session)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors(include_url=False))
    
@router.delete("/",
            openapi_extra={
                "requestBody": {
                    "content": {"application/x-yaml": {"schema": TaskSchema.DeleteTasksRequest.schema()}},
                    "required": True}})
async def delete_tasks(request: Request, Session = Depends(get_session)):
    raw_body = await request.body()
    try:
        data = yaml.safe_load(raw_body)
    except yaml.YAMLError:
        raise HTTPException(status_code=422, detail="Invalid YAML")
    try:
        task = TaskSchema.DeleteTasksRequest.model_validate(data)
        return task_service.delete_tasks(task, Session)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors(include_url=False))