from fastapi import Depends, APIRouter
from app.models.user import User
from app.database import get_session
from app.schemas.user import *
from sqlmodel import select

router = APIRouter()

@router.post("/")
def create_account(request: PostAccountRequest,
                   Session = Depends(get_session)):
    if request.login is not None and request.password is not None:
        if select(User).where(User.login == request.login):
            return {"status": "failure", 
                    "message": "Login already taken"}
        else:
            user = User(login=request.login, 
                        password=request.password)
            Session.add(user)
            Session.commit()
            Session.refresh(user)
            return {"status": "sucess", 
                    "user": user}
    else:
        return {"status": "failure", 
                "message": "Dont get login or password"}

@router.get("/{user_id}/")
def get_account(user_id: int, 
                Session = Depends(get_session)):
    user = select(User).where(User.id == user_id)
    if user:
        return {"status": "sucess", 
                "user": user}
    else:
        return {"status": "failure", 
                "message": "User not found"}