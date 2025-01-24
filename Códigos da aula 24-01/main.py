




from fastapi import FastAPI, HTTPException
from crud import create_item, get_all_items, get_item, update_item, delete_item
from schemas import ItemCreate, Item


app = FastAPI()

@app.post("/items/", response_model=str)
def create(data: ItemCreate):
    item_id = create_item(data.model_dump())
    return item_id

@app.get("/items/", response_model=list[Item])
def read_all():
    items = get_all_items()
    return items


@app.get("/items/", response_model=Item)
def read(item_id: str):
    item = get_item(item_id)
    
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return item


@app.put("/items/{item_id}", response_model=Item)
def update(item_id: str, data: ItemCreate):
    item_update = update_item(item_id, data.model_dump())
    
    if not item_update:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return item_update


@app.delete("/items/{item_id}")
def delete(item_id: str):
    deleted_count = delete_item(item_id)
    
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return {"message": "Item deleted"} 
