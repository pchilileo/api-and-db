from fastapi import Depends, APIRouter
from app.models.task import Task
from app.database import get_session
from app.schemas.task import *


router = APIRouter()

@router.post("/")
def create_tasks(request: PostTaskRequest,
                Session = Depends(get_session)):
    task = Task(user_id = request.user_id, 
                name=request.name, 
                description=request.description, 
                deadline=request.deadline, 
                status=request.status)
    Session.add(task)
    Session.commit()
    Session.refresh(task)
    return {"status": "succes", 
            "task": task}
    
@router.put("/")
def update_tasks(request: PutTasksRequest,
                Session = Depends(get_session)):
    task = Session.query(Task).filter(Task.id == request.task_id).first()
    if task: ## ASK HOW
        if request.name is not None:
            task.name = request.name
        if request.description is not None:
            task.description = request.description
        if request.deadline is not None:
            task.deadline = request.deadline
        if request.status is not None:
            task.status = request.status
        Session.commit()
        Session.refresh(task)
        return {"status": "succes", 
                "task": task}
    else:
        return {"status": "failure", 
                "message": "Task not found"}

@router.get("/")
def get_tasks(task_id: Optional[int] = None,
              user_id: Optional[int] = None,
              Session = Depends(get_session)):
    if task_id is not None or user_id is not None:
        if task_id:
            task = Session.query(Task).filter(Task.id == task_id).first()
            if task:
                return  {"status": "success", 
                        "task": task}
            else:
                return  {"status": "failure", 
                        "message": "Task not found"}
        else:
            tasks = Session.query(Task).filter(Task.user_id == user_id).all()
        if tasks:
            return {"status": "success", 
                    "task": tasks}
        else:
            return {"status": "failure", 
                    "message": "User not found"}
    else:
        return {"status": "failure", 
                "message": "Dont have user_id or task_id"}
    
@router.delete("/")
def delete_tasks(request: DeleteTasksRequest, 
                 Session = Depends(get_session)):
    
    if request.task_id:
        task = Session.query(Task).filter(Task.id == request.task_id).first()
        if task:
            Session.delete(task)
            Session.commit()
            return {"status": "success", 
                    "message": "Task deleted"}
        else:
            return {"status": "failure", 
                    "message": "Task not found"}
    else:
        tasks = Session.query(Task).filter(Task.user_id == request.user_id).all()
        if tasks:
            for task in tasks:
                Session.delete(task)
            Session.commit()
            return {"status": "success", 
                    "message": "All tasks deleted for user"}
        else:
            return {"status": "failure", 
                    "message": "User not found"}