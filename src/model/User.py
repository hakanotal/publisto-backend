from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    id: Optional[int] = None
    is_admin: Optional[bool] = False
    name: str
    email: str
    hashed_password: str

class UserSignUp(BaseModel):
    name: str
    email: str
    password: str

class UserSignIn(BaseModel):
    email: str
    password: str

class UserDelete(BaseModel):
    id: int