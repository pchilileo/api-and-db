from fastapi import Depends, APIRouter
from app.models.user import User
from app.database import get_session
from sqlmodel import select
import app.services.user_service as user_service

router = APIRouter()

@router.get("/accounts/")
def get_accounts(session = Depends(get_session)):
    users = select(User).all()
    return users