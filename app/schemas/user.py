from pydantic import BaseModel
from typing import Optional

class PostAccountRequest(BaseModel):
    login: Optional[str]
    password: Optional[str]