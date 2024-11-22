from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import xml.etree.ElementTree as ET
import os

app = FastAPI()
XML_FILE = "database.xml"

# Modelo de dados para o produto
class Produto(BaseModel):
    id: int
    nome: str
    preco: float
    quantidade: int

# Função para ler os dados do XML
def ler_dados_xml():
    produtos = []
    if os.path.exists(XML_FILE):
        tree = ET.parse(XML_FILE)
        root = tree.getroot()
        for elem in root.findall("produto"):
            produto = Produto(
                id=int(elem.find("id").text),
                nome=elem.find("nome").text,
                preco=float(elem.find("preco").text),
                quantidade=int(elem.find("quantidade").text)
            )
            produtos.append(produto)
    return produtos

# Função para escrever os dados no XML
def escrever_dados_xml(produtos):
    root = ET.Element("produtos")
    for produto in produtos:
        produto_elem = ET.SubElement(root, "produto")
        ET.SubElement(produto_elem, "id").text = str(produto.id)
        ET.SubElement(produto_elem, "nome").text = produto.nome
        ET.SubElement(produto_elem, "preco").text = str(produto.preco)
        ET.SubElement(produto_elem, "quantidade").text = str(produto.quantidade)

    tree = ET.ElementTree(root)
    tree.write(XML_FILE)

# Rota para obter todos os produtos
@app.get("/produtos", response_model=list[Produto])
def listar_produtos():
    return ler_dados_xml()

# Rota para obter um produto por ID
@app.get("/produtos/{produto_id}", response_model=Produto)
def obter_produto(produto_id: int):
    produtos = ler_dados_xml()
    for produto in produtos:
        if produto.id == produto_id:
            return produto
    raise HTTPException(status_code=404, detail="Produto não encontrado")

# Rota para criar um novo produto
@app.post("/produtos", response_model=Produto)
def criar_produto(produto: Produto):
    produtos = ler_dados_xml()
    if any(p.id == produto.id for p in produtos):
        raise HTTPException(status_code=400, detail="ID já existe")
    produtos.append(produto)
    escrever_dados_xml(produtos)
    return produto

# Rota para atualizar um produto
@app.put("/produtos/{produto_id}", response_model=Produto)
def atualizar_produto(produto_id: int, produto_atualizado: Produto):
    produtos = ler_dados_xml()
    for i, produto in enumerate(produtos):
        if produto.id == produto_id:
            produtos[i] = produto_atualizado
            escrever_dados_xml(produtos)
            return produto_atualizado
    raise HTTPException(status_code=404, detail="Produto não encontrado")

# Rota para deletar um produto
@app.delete("/produtos/{produto_id}", response_model=dict)
def deletar_produto(produto_id: int):
    produtos = ler_dados_xml()
    produtos_filtrados = [produto for produto in produtos if produto.id != produto_id]
    if len(produtos) == len(produtos_filtrados):
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    escrever_dados_xml(produtos_filtrados)
    return {"mensagem": "Produto deletado com sucesso"}
