from fastapi.responses import JSONResponse
from app.models.task import Task
from app.models.user import User
import app.schemas.task as TaskSchema
from sqlmodel import select

def create_tasks(request: TaskSchema.PostTaskRequest,
                 Session):
    task = Task(user_id = request.user_id, 
                name=request.name, 
                description=request.description, 
                deadline=request.deadline, 
                status=request.status)
    if Session.exec(select(User).where(User.id == request.user_id)).first() is None:
        return JSONResponse(
            status_code=400,
            content={"status": "failure",
                     "message": "User not found"})
    Session.add(task)
    Session.commit()
    Session.refresh(task)
    return JSONResponse(
        status_code=201,
        content={"status": "success",
                 "task": task.dict()})

def update_tasks(request: TaskSchema.PutTasksRequest,
                 Session):
    task = Session.exec(select(Task).where(Task.id == request.task_id)).first()
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
        return JSONResponse(status_code=201,
                            content={"status": "sucess", 
                                     "task": task.dict()})
    return JSONResponse(status_code=404,
                        content={"status": "failure", 
                                 "message": "Task not found"})
    
def get_tasks(task_request: TaskSchema.GetTaskRequest, 
              Session):
    if task_request.task_id is not None or task_request.user_id is not None:
        if task_request.task_id:
            task = Session.exec(select(Task).where(Task.id == task_request.task_id)).first()
            if task:
                return JSONResponse(status_code=200,
                                    content={"status": "success", 
                                    "task": task.dict()})
            return JSONResponse(status_code=404,
                                content={"status": "failure", 
                                         "message": "Task not found"})
        tasks = Session.exec(select(Task).where(Task.user_id == task_request.user_id)).all()
        if tasks:
            return JSONResponse(status_code=200,
                                content={"status": "success", 
                                         "task": [task.dict() for task in tasks]})
        return JSONResponse(status_code=404,
                            content={"status": "failure", 
                                     "message": "User not found"})
    return JSONResponse(status_code=400,
                        content={"status": "failure", 
                                 "message": "Dont have user_id or task_id"})

def delete_tasks(request: TaskSchema.DeleteTasksRequest, 
                 Session):
    if request.task_id:
        task = Session.exec(select(Task).where(Task.id == request.task_id)).first()
        if task is not None:
            Session.delete(task)
            Session.commit()
            return JSONResponse(status_code=200,
                                content={"status": "success", 
                                         "message": "Task deleted"})
        return JSONResponse(status_code=404,
                            content={"status": "failure", 
                                     "message": "Task not found"})
    tasks = Session.exec(select(Task).where(Task.user_id == request.user_id)).all()
    if tasks:
        for task in tasks:
            Session.delete(task)
        Session.commit()
        return JSONResponse(status_code=200,
                            content={"status": "success", 
                                     "message": "All tasks deleted for user"})
    return JSONResponse(status_code=404,
                        content={"status": "failure", 
                                 "message": "User not found"})