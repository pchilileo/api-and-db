from fastapi import Depends, APIRouter
from app.models.task import Task
from app.database import get_session
from sqlmodel import select

router = APIRouter()

@router.get("/tasks/")
def get_tasks(Session = Depends(get_session)):
    tasks = select(Task).all()
    return tasks