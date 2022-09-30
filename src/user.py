from fastapi import APIRouter
from .database import Database
from pydantic import BaseModel
from .utils import hash_password


class User(BaseModel):
    username: str
    email: str
    password: str

class UserInDB(BaseModel):
    username: str
    email: str
    hashed_password: str

router = APIRouter()

@router.get("/users/all")
async def get_users():
    users = Database.get_users()
    return users

@router.post("/users/create")
async def create_user(user: User):
    newUser = UserInDB(**user.dict(), hashed_password=hash_password(user.password))
    return Database.create_user(newUser)
    