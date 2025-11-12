from fastapi import Depends, APIRouter, Path
from typing import Annotated

from app.database import get_session
import app.schemas.user as UserSchema
import app.services.user_Service as user_Service


router = APIRouter()

@router.put("/",
            response_model=UserSchema.AccountResponse,
            status_code=200)   
async def update_password(request: UserSchema.AccountRequest,
                          session = Depends(get_session)
) -> UserSchema.AccountResponse:
    user = user_Service.update_password(request, session)
    return user

@router.get("/{user_id}/",
            response_model=UserSchema.AccountResponse,
            status_code=200)
async def get_account(user_id: Annotated[int, Path(gt=0)], 
                session = Depends(get_session)
) -> UserSchema.AccountResponse:
    user = user_Service.get_account(user_id, session)
    return user

## TODO
## PUT /users/me — Обновить свой профиль, users.py
## GET /users/me — Получить свой профиль, users.py