from pydantic import BaseModel

class ItemCreate(BaseModel):
    name: str
    description: str
    price: float
    in_stock: bool


class Item(ItemCreate):
    id: str


