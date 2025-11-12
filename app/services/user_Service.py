from fastapi import HTTPException
from sqlmodel import select, Session

from app.models.user import User
import app.database as database
import app.schemas.user as UserSchema


def update_password(
        request: UserSchema.AccountRequest,
        session: Session
) -> User:
    statement = select(User).where(User.login == request.login)
    user = session.exec(statement).first()
    if not user:
        raise HTTPException(status_code=404, 
                            detail="User not found")
    user.password = request.password
    database.add_commit_refresh(session, user)
    return user

def get_account(
        user_id: int, 
        session: Session
) -> User:
    statement = select(User).where(User.id == user_id)
    user = session.exec(statement).first()
    if not user:
        raise HTTPException(status_code=404, 
                            detail="User not found")
    return user
    