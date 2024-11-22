from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import csv
import os

app = FastAPI()
CSV_FILE = "database.csv"

# Modelo de dados para o produto
class Produto(BaseModel):
    id: int
    nome: str
    preco: float
    quantidade: int

# Função para ler os dados do CSV
def ler_dados_csv():
    produtos = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode="r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                produtos.append(Produto(**row))
    return produtos

# Função para escrever os dados no CSV
def escrever_dados_csv(produtos):
    with open(CSV_FILE, mode="w", newline="") as file:
        fieldnames = ["id", "nome", "preco", "quantidade"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for produto in produtos:
            writer.writerow(produto.dict())

# Rota para obter todos os produtos
@app.get("/produtos", response_model=list[Produto])
def listar_produtos():
    return ler_dados_csv()

# Rota para obter um produto por ID
@app.get("/produtos/{produto_id}", response_model=Produto)
def obter_produto(produto_id: int):
    produtos = ler_dados_csv()
    for produto in produtos:
        if produto.id == produto_id:
            return produto
    raise HTTPException(status_code=404, detail="Produto não encontrado")

# Rota para criar um novo produto
@app.post("/produtos", response_model=Produto)
def criar_produto(produto: Produto):
    produtos = ler_dados_csv()
    if any(p.id == produto.id for p in produtos):
        raise HTTPException(status_code=400, detail="ID já existe")
    produtos.append(produto)
    escrever_dados_csv(produtos)
    return produto

# Rota para atualizar um produto
@app.put("/produtos/{produto_id}", response_model=Produto)
def atualizar_produto(produto_id: int, produto_atualizado: Produto):
    produtos = ler_dados_csv()
    for i, produto in enumerate(produtos):
        if produto.id == produto_id:
            produtos[i] = produto_atualizado
            escrever_dados_csv(produtos)
            return produto_atualizado
    raise HTTPException(status_code=404, detail="Produto não encontrado")

# Rota para deletar um produto
@app.delete("/produtos/{produto_id}", response_model=dict)
def deletar_produto(produto_id: int):
    produtos = ler_dados_csv()
    produtos_filtrados = [produto for produto in produtos if produto.id != produto_id]
    if len(produtos) == len(produtos_filtrados):
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    escrever_dados_csv(produtos_filtrados)
    return {"mensagem": "Produto deletado com sucesso"}
