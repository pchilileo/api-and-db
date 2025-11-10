from pydantic import BaseModel

class PostAccountRequest(BaseModel):
    login: str
    password: str

class PutAccountRequest(BaseModel): ## For future updates
    login: str
    password: str