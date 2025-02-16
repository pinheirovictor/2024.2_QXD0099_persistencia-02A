from fastapi import FastAPI, HTTPException
from firebase_config import db
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Item(BaseModel):
    nome: str
    descricao: Optional[str] = None
    preco: float

# Rota para criar um item
@app.post("/items/")
async def criar_item(item: Item):
    doc_ref = db.collection("items").document()
    doc_ref.set(item.dict())
    return {"id": doc_ref.id, "mensagem": "Item criado com sucesso"}

# Rota para listar todos os itens
@app.get("/items/")
async def listar_itens():
    itens_ref = db.collection("items").stream()
    itens = [{**item.to_dict(), "id": item.id} for item in itens_ref]
    return {"items": itens}

# Rota para obter um item pelo ID
@app.get("/items/{item_id}")
async def obter_item(item_id: str):
    doc_ref = db.collection("items").document(item_id)
    doc = doc_ref.get()
    if doc.exists:
        return {**doc.to_dict(), "id": item_id}
    raise HTTPException(status_code=404, detail="Item não encontrado")

# Rota para atualizar um item
@app.put("/items/{item_id}")
async def atualizar_item(item_id: str, item: Item):
    doc_ref = db.collection("items").document(item_id)
    if not doc_ref.get().exists:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    doc_ref.update(item.dict())
    return {"mensagem": "Item atualizado com sucesso"}

# Rota para deletar um item
@app.delete("/items/{item_id}")
async def deletar_item(item_id: str):
    doc_ref = db.collection("items").document(item_id)
    if not doc_ref.get().exists:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    doc_ref.delete()
    return {"mensagem": "Item deletado com sucesso"}
