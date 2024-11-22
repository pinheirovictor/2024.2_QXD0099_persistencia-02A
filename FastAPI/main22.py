from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

# Cria uma instância da aplicação FastAPI
app = FastAPI()

# Define o modelo de dados Item, que será utilizado para validar o corpo das requisições
class Item(BaseModel):
    nome: str                    # Nome do item (obrigatório)
    valor: float                 # Valor do item (obrigatório)
    is_oferta: Union[bool, None] = None  # Indica se o item está em oferta, valor opcional

# Dicionário para armazenar os itens, com o item_id como chave e o Item como valor
items_db = {}

# Endpoint raiz que retorna uma mensagem de boas-vindas
@app.get("/")
def read_root():
    return {"msg": "Hello World"}

# Endpoint para ler os dados de um item específico, baseado no item_id
@app.get("/itens/{item_id}")
def le_item(item_id: int):
    # Verifica se o item existe no dicionário items_db
    if item_id in items_db:
        return items_db[item_id]  # Retorna o item se encontrado
    else:
        return {"erro": "Item não encontrado"}  # Retorna uma mensagem de erro se o item não existir

# Endpoint para atualizar os dados de um item específico, baseado no item_id
@app.put("/itens/{item_id}")
def atualiza_item(item_id: int, item: Item):
    # Atualiza o item no dicionário items_db com o item_id fornecido
    items_db[item_id] = item
    # Retorna uma mensagem de sucesso e os dados do item atualizado
    return {"mensagem": "Item atualizado com sucesso", "item": items_db[item_id]}
