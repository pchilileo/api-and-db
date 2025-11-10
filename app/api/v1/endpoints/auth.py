from fastapi import Depends, APIRouter
from app.models.user import User
from app.database import get_session
from sqlmodel import select

router = APIRouter()

@router.post("/")
def authenticate(login: str, 
                 password: str,
                 Session = Depends(get_session)):
    user = select(User).where(User.login == login, User.password == password)
    if user:
        return {"status": "success", "user_id": user.id}
    else:
        return {"status": "failure", "message": "Invalid credentials"}