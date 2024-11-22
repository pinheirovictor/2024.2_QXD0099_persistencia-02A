from typing import Union
from fastapi import FastAPI

# Cria uma instância da aplicação FastAPI
app = FastAPI()

# Endpoint raiz que retorna uma mensagem de boas-vindas
@app.get("/")
def read_root():
    # Retorna uma mensagem padrão como resposta
    return {"msg": "Hello World"}

# Endpoint para ler os dados de um item específico, com base no item_id e um nome opcional
@app.get("/itens/{item_id}")
def read_item(item_id: int, nome: Union[str, None] = None):
    # Retorna o ID do item e o nome, caso tenha sido fornecido
    return {"item_id": item_id, "nome": nome}

