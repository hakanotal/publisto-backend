from typing import Optional
from pydantic import BaseModel

class List(BaseModel):
    id: Optional[int] = None
    user_id: int
    updated_at: str
    items: list[str]
    items_size: int
    is_active: bool

class ListCreate(BaseModel):
    items: list[str]
    items_size: int
    is_active: bool

class ListUpdate(BaseModel):
    id: int
    items: list[str]
    items_size: int
    is_active: bool

class ListDelete(BaseModel):
    id: int