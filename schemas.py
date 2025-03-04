from pydantic import BaseModel
from fastapi import Form

class UserSchemaIn(BaseModel):
    username: str
    password: str

    @classmethod
    def as_form(cls, username: str = Form(...), password: str = Form(...)):
        return cls(username=username, password=password)

class UserSchemaOut(BaseModel):
    id: int
    username: str
    avatar: str | None = None

    class Config:
        from_attributes = True