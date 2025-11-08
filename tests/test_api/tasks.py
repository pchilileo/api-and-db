from fastapi import Depends, APIRouter
from app.models.task import Task
from app.database import get_session

router = APIRouter()

@router.get("/tasks/")
def get_tasks(Session = Depends(get_session)):
    tasks = Session.query(Task).all()
    return tasks