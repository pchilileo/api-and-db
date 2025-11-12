from sqlmodel import select, Session
from fastapi import HTTPException

from app.models.task import Task
from app.models.user import User
import app.schemas.task as TaskSchema
import app.database as database

def create_tasks(request: TaskSchema.PostTaskRequest, session: Session
) -> Task:
    statement = select(User).where(User.id == request.user_id)
    user = session.exec(statement).first()
    if not user:
        raise HTTPException(status_code=404, 
                            detail="User not found")

    task = Task(user_id = request.user_id, 
                name=request.name, 
                description=request.description, 
                deadline=request.deadline, 
                status=request.status)

    database.add_commit_refresh(session, task)
    return task

def update_tasks(request: TaskSchema.PutTasksRequest,
                 session: Session
) -> Task:
    statement = select(Task).where(Task.id == request.task_id)
    task = session.exec(statement).first()
    if not task: 
        raise HTTPException(status_code=404,
                            detail="Task not found")
    update_data = request.model_dump(exclude_unset=True, exclude={"task_id"})
    for key, value in update_data.items():
        setattr(task, key, value)
        task.deadline = request.deadline
    database.add_commit_refresh(session, task)
    return task

def get_tasks(user_id: int, 
              task_id: int | None,
              session: Session
) -> list[Task] | Task:
    if user_id is None:
        raise HTTPException(status_code=400,
                            detail="Undefined user_id")
    statement = select(Task).where(Task.user_id == user_id)
    tasks = session.exec(statement).all()
    if not tasks:
        raise HTTPException(status_code=404,
                            detail=f"Tasks for user_id: {user_id} not found")
    if task_id is None:
        return tasks
    statement = select(Task).where(Task.id == task_id)
    task = session.exec(statement).first()
    if task:
        return task
    raise HTTPException(status_code=404,
                    detail=f"Task task_id:{task_id} not found")
    
def delete_tasks(user_id: int, 
                 task_id: int | None,
                 session: Session) -> None:
    if user_id is None:
        raise HTTPException(status_code=400,
                            detail="Undefined user_id")
    statement = select(Task).where(Task.user_id == user_id)
    tasks = session.exec(statement).all()
    if not tasks:
        raise HTTPException(status_code=404,
                            detail="User not found")
    if task_id is None:
        for task in tasks:
            session.delete(task)
        return
    statement = select(Task).where(Task.id == task_id)
    task = session.exec(statement).first()
    if task:
        session.delete(task)
        return
    raise HTTPException(status_code=404,
                    detail=f"Task task_id:{task_id} not found")