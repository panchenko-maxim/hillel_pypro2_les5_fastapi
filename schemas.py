from pydantic import BaseModel

class UserSchemaIn(BaseModel):
    username: str
    password: str

class UserSchemaOut(BaseModel):
    id: int
    username: str
    avatar: str | None = None

    class Config:
        from_attributes = True