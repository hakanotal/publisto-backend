from typing import Optional
from unicodedata import name
from pydantic import BaseModel
from .Item import Item

class List(BaseModel):
    id: Optional[int] = None
    user_id: int
    updated_at: str
    name: str
    items: list[Item]
    is_active: bool
    is_public: bool

class ListCreate(BaseModel):
    name: str
    items: list[Item]
    is_active: bool = True
    is_public: bool = False

class ListUpdate(BaseModel):
    id: int
    name: str
    items: list[Item]
    is_active: bool = True
    is_public: bool = False

class ListWithId(BaseModel):
    id: int