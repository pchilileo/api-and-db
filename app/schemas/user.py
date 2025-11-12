from pydantic import BaseModel, ConfigDict, Field
from typing import Annotated

class AccountBase(BaseModel):
    login: Annotated[str, Field(min_length=8, max_length=32)]
    password: Annotated[str, Field(min_length=8, max_length=32)]

class AccountRequest(AccountBase):
    pass

class AccountResponse(AccountBase):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "user_id": 1,
                "login": "Example Login",
                "password": "Example Password"
            }
        }
    )