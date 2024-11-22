from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

# Cria uma instância da aplicação FastAPI
app = FastAPI()

# Define o modelo de dados Item, que será utilizado para validar o corpo das requisições
class Item(BaseModel):
    nome: str                # Nome do item (obrigatório)
    valor: float             # Valor do item (obrigatório)
    is_oferta: Union[bool, None] = None  # Indica se o item está em oferta, valor opcional

# Endpoint raiz que retorna uma mensagem de boas-vindas
@app.get("/")
def read_root():
    return {"msg": "Hello World"}

# Endpoint que lê os dados de um item específico, baseado no ID e nome opcional
@app.get("/itens/{item_id}")
def le_item(item_id: int, nome: Union[str, None] = None):
    # Retorna o ID do item e o nome (se fornecido)
    return {"item_id": item_id, "nome": nome}

# Endpoint que atualiza os dados de um item específico baseado no ID e nos novos dados do item
@app.put("/itens/{item_id}")
def atualiza_item(item_id: int, item: Item):
    # Retorna o nome do item atualizado e o ID do item
    return {"item_nome": item.nome, "item_id": item_id}
