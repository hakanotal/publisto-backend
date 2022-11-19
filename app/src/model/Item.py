from typing import Optional
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    amount: int
    bought_by: Optional[str] = None
