from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from typing import Optional
from .database import Database
from pydantic import BaseModel
from .user import User, decode_token


auth_scheme = HTTPBearer()
router = APIRouter(prefix="/list",tags=["LIST"])

class List(BaseModel):
    user_id: int
    created_at: str
    updated_at: Optional[str]
    items: list[str]
    items_size: int
    is_active: bool


@router.get("/all", response_model=list[List])
async def get_all_lists(user: User = Depends(decode_token)):
    if user.is_admin:
        print("[LIST ALL]", user)
        allLists = Database.get_lists()
        return allLists.data

@router.post("/user", response_model=list[List])
async def get_lists_of_a_user(user: User = Depends(decode_token)):
    print("[LIST USER]", user)
    lists = Database.get_lists_by_user_id(user.id)
    return lists.data

@router.post("/active", response_model=List)
async def get_active_list_of_a_user(user: User = Depends(decode_token)):
    print("[LIST ACTIVE]", user)
    lists = Database.get_active_lists_by_user_id(user.id)
    return lists.data[0]