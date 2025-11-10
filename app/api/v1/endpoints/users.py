from fastapi import Depends, APIRouter, HTTPException, Request
from pydantic import ValidationError
from app.database import get_session
import app.schemas.user as UserSchema
import app.services.user_service as user_service
import json

router = APIRouter()

@router.post("/",
             openapi_extra={
                 "requestBody": {
                     "content": {"application/x-json": {"schema": UserSchema.PostAccountRequest.model_json_schema()}},
                     "required": True}})   
async def create_account(request: Request,
                         session = Depends(get_session)):
    raw_body = await request.body()
    try:
        data = json.loads(raw_body)
    except json.JSONDecodeError:
        raise HTTPException(status_code=422, detail="Invalid JSON")
    try:
        user = UserSchema.PostAccountRequest.model_validate(data)
        return user_service.create_account(user, session)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors(include_url=False))

@router.put("/",
             openapi_extra={
                 "requestBody": {
                     "content": {"application/x-json": {"schema": UserSchema.PutAccountRequest.model_json_schema()}},
                     "required": True}})   
async def update_password(request: Request,
                          session = Depends(get_session)):
    raw_body = await request.body()
    try:
        data = json.loads(raw_body)
    except json.JSONDecodeError:
        raise HTTPException(status_code=422, detail="Invalid JSON")
    try:
        user = UserSchema.PutAccountRequest.model_validate(data)
        return user_service.update_password(user, session)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors(include_url=False))

@router.get("/{user_id}/")
async def get_account(user_id: int, 
                session = Depends(get_session)):
    return user_service.get_account(user_id, session)