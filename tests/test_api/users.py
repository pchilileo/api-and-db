from fastapi import Depends, APIRouter
from app.models.user import User
from app.database import get_session

router = APIRouter()

@router.get("/accounts/")
def get_accounts(Session = Depends(get_session)):
    users = Session.query(User).all()
    return users