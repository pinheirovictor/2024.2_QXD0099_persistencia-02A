

from pydantic import BaseModel
from typing import Optional

class ItemModel(BaseModel):
    id: Optional[str]
    name: str
    description: str
    price: float
    in_stock: bool

