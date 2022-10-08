from typing import Optional
from pydantic import BaseModel

class List(BaseModel):
    user_id: int
    created_at: str
    updated_at: Optional[str]
    items: list[str]
    items_size: int
    is_active: bool