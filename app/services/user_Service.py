from fastapi import Depends
from fastapi.responses import JSONResponse
from app.models.user import User
from app.database import get_session
import app.schemas.user as UserSchema
from sqlmodel import select

def create_account(request: UserSchema.PostAccountRequest,
                   session = Depends(get_session)):
    if request.login is not None and request.password is not None:
        if session.exec(select(User).where(User.login == request.login)).first() is None:
            user = User(login=request.login, 
                        password=request.password)
            session.add(user)
            return JSONResponse(status_code=201,
                                content={"status": "success", 
                                         "message": "Account created successfully"})
        return JSONResponse(status_code=409,
                        content={"status": "failure", 
                                 "message": "Login already exists"})
    return JSONResponse(status_code=400,
                        content={"status": "failure", 
                                 "message": "Undefined login or password"})
    
def update_password(request: UserSchema.PutAccountRequest,
                    session = Depends(get_session)):
    user = session.exec(select(User).where(User.login == request.login)).first()
    if user:
        user.password = request.password
        return JSONResponse(status_code=200,
                            content={"status": "success", 
                                     "message": "Password updated successfully"})
    return JSONResponse(status_code=404,
                        content={"status": "failure", 
                                 "message": "User not found", 
                                 "detail": "Use correct login"})

def get_account(user_id: int, 
                session = Depends(get_session)):
    user = session.exec(select(User).where(User.id == user_id)).first()
    if user:
        return JSONResponse(status_code=200,
                            content={"status": "success", 
                                     "user": user.dict()})
    return JSONResponse(status_code=404,
                        content={"status": "failure", 
                                 "message": "User not found"})