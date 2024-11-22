from fastapi import FastAPI, HTTPException 
from http import HTTPStatus
from pydantic import BaseModel
import csv
import os

app = FastAPI()
csv_FILE = "database.csv"

#Modelo de dados
class Produto(BaseModel):
        id: int
        nome: str
        preco: float
        quantidade: int

# Ler os dados do CSV
def ler_dados_csv():
    produtos = []
    if os.path.exists(csv_FILE):
        with open (csv_FILE, mode="r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                produtos.append(Produto(**row))
    return produtos


#Escrever os dados
def escrever_dados_csv(produtos):
    with open(csv_FILE, mode="w", newline="") as file:
        fieldnames = ["id", "nome", "preco", "quantidade"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for produto in produtos:
            writer.writerow(produto.dict())

@app.get("/produtos", response_model=list[Produto])
def listar_produtos():
        return ler_dados_csv()
    
@app.get("/produtos/{id}")
def get_products_by_id(id:int):
    products = ler_dados_csv()
    
    for product in products:
        if product.id == id:
            return product
    raise HTTPException(status_code=404, detail="Item nao encontrado")

@app.post("/produtos",response_model=Produto, status_code=HTTPStatus.CREATED )
def criar_produto(produto:Produto):
    produtos = ler_dados_csv()
    
    if any(p.id == produto.id for p in produtos):
        raise HTTPException(status_code=400,detail="Produto já existente")
    produtos.append(produto)
    escrever_dados_csv(produtos)
    return produto
    
@app.put("/produtos/{id}",response_model=Produto)
def atualizar_produto(id:int, produtoAtualizado:Produto):
    produtos = ler_dados_csv()
    for i , produto in enumerate(produtos):
        if produto.id == id:
            produtos[i] = produtoAtualizado
            escrever_dados_csv(produtos)
            return produtoAtualizado
    raise HTTPException(status_code=404,detail="Produto não encontrado")

@app.delete("/produtos2/{id}", status_code=HTTPStatus.NO_CONTENT)
def remover_produto(id:int):
    produtos = ler_dados_csv()
    for i, produto in enumerate(produtos):
        if produto.id == id:
            produtos.pop(i)
            escrever_dados_csv(produtos)
            return {
                        "id": id,
                        "message" : "Produto deletado"
                    }
    raise HTTPException(status_code=404, detail="Produto não encontrado")

@app.delete("/produtos/{id}", status_code=HTTPStatus.NO_CONTENT)
def remover_produto2(id:int):
    produtos = ler_dados_csv()
    produtos_filtrados = [produto for produto in produtos if produto.id == id]
    if len(produtos) == len(produtos_filtrados):
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    escrever_dados_csv(produtos_filtrados)
    return {"message" : "Produto deletado"}
     