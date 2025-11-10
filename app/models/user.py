from sqlmodel import Field, SQLModel, Relationship
from typing import List

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    login: str
    password: str

    tasks: List["Task"] = Relationship(back_populates="user") # type: ignore