from fastapi import FastAPI
from sqlmodel import Session, create_engine, SQLModel
from app.models.user import User
from app.models.task import Task

app = FastAPI(title="testdb")
engine = create_engine("sqlite:///database.db")
SQLModel.metadata.create_all(engine)

## Account
@app.post("/account/create/")
def create_account(login: str, password: str):
    with Session(engine) as session:
        user = User(login=login, password=password)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

@app.get("/account/get/{user_id}/")
def get_account_info(user_id: int):
    with Session(engine) as session:
        user = session.query(User).filter(User.id == user_id).first()
        if user:
            return user
        else:
            return {"status": "failure", "message": "User not found"}
    
## Task
@app.post("/task/create/")
def create_task(user_id: int, name: str, description: str | None = None, deadline: str | None = None):
    with Session(engine) as session:
        task = Task(user_id=user_id, name=name, description=description, deadline=deadline)
        session.add(task)
        session.commit()
        session.refresh(task)
        return task
    
@app.delete("/task/delete/{task_id}/")
def delete_task(task_id: int):
    with Session(engine) as session:
        task = session.query(Task).filter(Task.id == task_id).first()
        if task:
            session.delete(task)
            session.commit()
            return {"status": "success", "message": "Task deleted"}
        else:
            return {"status": "failure", "message": "Task not found"}

@app.get("/task/get/all/{user_id}/")
def get_tasks_for_account(user_id: int):
    with Session(engine) as session:
        tasks = session.query(Task).filter(Task.user_id == user_id).all()
        return tasks
    
@app.post("/task/update/info/{task_id}/")
def update_task(task_id: int, name: str | None = None, description: str | None = None, deadline: str | None = None):
    with Session(engine) as session:
        task = session.query(Task).filter(Task.id == task_id).first()
        if task:
            if name is not None:
                task.name = name
            if description is not None:
                task.description = description
            if deadline is not None:
                task.deadline = deadline
            session.commit()
            session.refresh(task)
            return task
        else:
            return {"status": "failure", "message": "Task not found"}

@app.post("/task/update/status/{task_id}/")
def update_task_status(task_id: int, status: bool):
    with Session(engine) as session:
        task = session.query(Task).filter(Task.id == task_id).first()
        if task:
            task.status = status
            session.commit()
            session.refresh(task)
            return task
        else:
            return {"status": "failure", "message": "Task not found"}
        
   
    with Session(engine) as session:
        tasks = session.query(Task).filter(Task.user_id == user_id).all()
        for task in tasks:
            session.delete(task)
        session.commit()
        return {"status": "success", "message": "All tasks deleted for user"}

## Authentication
@app.post("/auth/")
def authenticate(login: str, password: str):

    with Session(engine) as session:
        user = session.query(User).filter(User.login == login, User.password == password).first()
        if user:
            return {"status": "success", "user_id": user.id}
        else:
            return {"status": "failure", "message": "Invalid credentials"}
        
## Test
@app.get("/get-accounts/")
def get__all_accounts():
    with Session(engine) as session:
        users = session.query(User).all()
        return users
    
@app.get("/get-tasks/")
def get__all_tasks():
    with Session(engine) as session:
        tasks = session.query(Task).all()
        return tasks