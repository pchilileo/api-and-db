from fastapi import HTTPException
from sqlmodel import select, Session

from app.models.user import User
import app.database as database
import app.schemas.user as UserSchema



def create_account(
        request: UserSchema.AccountRequest,      
        session: Session 
) -> User:
    if request.login is None or request.password is None:
        raise HTTPException(
            status_code=422, 
            detail="Undefined login or password"
        )
    statement = select(User).where(User.login == request.login)
    result = session.exec(statement).first()
    if result:
        raise HTTPException(
            status_code=409,
            detail="Login already exists"
        )
    ## TODO ADD HASH PASSWORD
    user = User(login=request.login, password=request.password)
    database.add_commit_refresh(session, user)
    return user