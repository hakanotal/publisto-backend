from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    id: Optional[int] = None
    is_admin: Optional[bool] = False
    name: str
    email: str
    hashed_password: str

class UserProfile(BaseModel):
    id: int
    name: str
    email: str

class UserSignUp(BaseModel):
    name: str
    email: str
    password: str

class UserSignIn(BaseModel):
    email: str
    password: str

class UserWithEmail(BaseModel):
    email: str

class UserWithId(BaseModel):
    id: int

class UserForgot(BaseModel):
    email: str
    password: str
    code: str