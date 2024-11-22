from typing import Union, List
from http import HTTPStatus
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Cria uma instância da aplicação FastAPI
app = FastAPI()

# Define o modelo de dados Item, que será utilizado para validar o corpo das requisições
class Item(BaseModel):
    id: int                        # ID único do item
    nome: str                      # Nome do item (obrigatório)
    valor: float                   # Valor do item (obrigatório)
    is_oferta: Union[bool, None] = None  # Indica se o item está em oferta, valor opcional

# Lista para armazenar os itens, onde cada item é uma instância da classe Item
itens: List[Item] = []

# Endpoint raiz que retorna uma mensagem de boas-vindas
@app.get("/")
def padrao():
    # Retorna uma mensagem padrão como resposta
    return {"msg": "Hello World"}

# Endpoint para ler os dados de um item específico, com base no item_id
@app.get("/itens/{item_id}", response_model=Item)
def ler_item(item_id: int):
    # Itera sobre a lista de itens para encontrar o item com o ID especificado
    for indice, item_atual in enumerate(itens):
        if item_atual.id == item_id:
            return item_atual  # Retorna o item encontrado
    # Lança uma exceção se o item não for encontrado, com status 404
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Item não encontrado.")

# Endpoint para listar todos os itens
@app.get("/itens/", response_model=List[Item])
def listar_itens():
    # Retorna a lista de todos os itens armazenados
    return itens

# Endpoint para adicionar um novo item à lista
@app.post("/itens/", response_model=Item, status_code=HTTPStatus.CREATED)
def adicionar_item(item: Item):
    # Verifica se já existe um item com o mesmo ID
    if any(item_atual.id == item.id for item_atual in itens):
        # Lança uma exceção com status 400 se o ID já existe
        raise HTTPException(status_code=400, detail="ID já existe.")
    # Adiciona o novo item à lista de itens
    itens.append(item)
    return item  # Retorna o item adicionado

# Endpoint para atualizar os dados de um item específico, com base no item_id
@app.put("/itens/{item_id}", response_model=Item)
def atualizar_item(item_id: int, item_atualizado: Item):
    # Itera sobre a lista de itens para encontrar o item com o ID especificado
    for indice, item_atual in enumerate(itens):
        if item_atual.id == item_id:
            # Garante que o ID do item atualizado permanece o mesmo
            if item_atualizado.id != item_id:
                item_atualizado.id = item_id
            # Substitui o item existente pelo item atualizado
            itens[indice] = item_atualizado
            return item_atualizado  # Retorna o item atualizado
    # Lança uma exceção se o item não for encontrado, com status 404
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Item não encontrado.")

