from sqlmodel import Field, SQLModel, Relationship
from typing import Optional
from datetime import date

class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    name: str
    description: str | None = None
    deadline: date | None = None
    status: bool = Field(default=False) 

    user: Optional["User"] = Relationship(back_populates="tasks") # type: ignore