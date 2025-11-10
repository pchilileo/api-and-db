from fastapi.responses import JSONResponse
from app.models.task import Task
from app.models.user import User
import app.schemas.task as TaskSchema
from sqlmodel import select

def create_tasks(request: TaskSchema.PostTaskRequest,
                 session):
    task = Task(user_id = request.user_id, 
                name=request.name, 
                description=request.description, 
                deadline=request.deadline, 
                status=request.status)
    if session.exec(select(User).where(User.id == request.user_id)).first() is None:
        return JSONResponse(
            status_code=400,
            content={"status": "failure",
                     "message": "User not found"})
    session.add(task)
    return JSONResponse(
        status_code=201,
        content={"status": "success",
                 "task": task.dict()})

def update_tasks(request: TaskSchema.PutTasksRequest,
                 session):
    task = session.exec(select(Task).where(Task.id == request.task_id)).first()
    if task: ## ASK HOW
        if request.name is not None:
            task.name = request.name
        if request.description is not None:
            task.description = request.description
        if request.deadline is not None:
            task.deadline = request.deadline
        if request.status is not None:
            task.status = request.status
        return JSONResponse(status_code=200,
                            content={"status": "success", 
                                     "task": task.dict()})
    return JSONResponse(status_code=404,
                        content={"status": "failure", 
                                 "message": "Task not found"})
    
def get_tasks(user_id: int, task_id: int = None, session = None):
    if session is None:
        return JSONResponse(status_code=500,
                            content={"status": "failure", 
                                     "message": "Session not provided"})
    if user_id is not None:
        if task_id:
            task = session.exec(select(Task).where(Task.id == task_id)).first()
            if task:
                if task.user_id == user_id:
                    return JSONResponse(status_code=200,
                                        content={"status": "success", 
                                        "task": task.dict()})
                return JSONResponse(status_code=404,
                                    content={"status": "failure", 
                                            "message": "Task have another user_id"})
            return JSONResponse(status_code=404,
                                    content={"status": "failure", 
                                            "message": "Task not found"})
        tasks = session.exec(select(Task).where(Task.user_id == user_id)).all()
        if tasks:
            return JSONResponse(status_code=200,
                                content={"status": "success", 
                                         "task": [task.dict() for task in tasks]})
        return JSONResponse(status_code=404,
                            content={"status": "failure", 
                                     "message": "User not found"})
    return JSONResponse(status_code=400,
                        content={"status": "failure", 
                                 "message": "Undefined user_id"})

def delete_tasks(request: TaskSchema.DeleteTasksRequest, 
                 session):
    if request.task_id:
        task = session.exec(select(Task).where(Task.id == request.task_id)).first()
        if task is not None:
            session.delete(task)
            return JSONResponse(status_code=200,
                                content={"status": "success", 
                                         "message": "Task deleted"})
        return JSONResponse(status_code=404,
                            content={"status": "failure", 
                                     "message": "Task not found"})
    tasks = session.exec(select(Task).where(Task.user_id == request.user_id)).all()
    if tasks:
        for task in tasks:
            session.delete(task)
        return JSONResponse(status_code=200,
                            content={"status": "success", 
                                     "message": "All tasks deleted for user"})
    return JSONResponse(status_code=404,
                        content={"status": "failure", 
                                 "message": "User not found"})