from fastapi import Depends, APIRouter

from app.database import get_session
import app.schemas.user as UserSchema
import app.services.auth_Service as auth_Service

router = APIRouter()

## LEGACY CODE, TO BE UPDATED LATER
##@router.post("/")
##def authenticate(login: str, 
##                 password: str,
##                 session = Depends(get_session)):
##    user = select(User).where(User.login == login, User.password == password)
##    if user:
##        return {"status": "success", "user_id": user.id}
##    else:
##        return {"status": "failure", "message": "Invalid credentials"}
    
@router.post("/register/",
             response_model=UserSchema.AccountResponse,
             status_code=201,)   
async def create_account(request: UserSchema.AccountRequest,
                         session = Depends(get_session)
) -> UserSchema.AccountResponse:
    user = auth_Service.create_account(request, session)
    return user