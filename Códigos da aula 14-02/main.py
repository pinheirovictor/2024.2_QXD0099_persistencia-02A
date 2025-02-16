from fastapi import FastAPI, HTTPException
from firebase_config import db
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()

# ---------------------- DEFINIÇÃO DOS MODELOS ----------------------

# Modelo para representar uma categoria de itens
class Categoria(BaseModel):
    nome: str  # Nome da categoria
    descricao: Optional[str] = None  # Descrição opcional da categoria

# Modelo para representar um item, com um possível relacionamento com uma categoria
class Item(BaseModel):
    nome: str  # Nome do item
    descricao: Optional[str] = None  # Descrição opcional do item
    preco: float  # Preço do item
    categoria_id: Optional[str] = None  # ID da categoria à qual o item pertence





# ---------------------- ROTAS PARA CATEGORIAS ----------------------

# Criar uma nova categoria
@app.post("/categorias/")
async def criar_categoria(categoria: Categoria):
    """
    Cria uma nova categoria no banco de dados Firebase.
    """
    doc_ref = db.collection("categorias").document()  # Cria um novo documento
    doc_ref.set(categoria.model_dump())  # Salva os dados no Firestore
    return {"id": doc_ref.id, "mensagem": "Categoria criada com sucesso"}

# Listar todas as categorias
@app.get("/categorias/")
async def listar_categorias():
    """
    Retorna a lista de todas as categorias cadastradas.
    """
    categorias_ref = db.collection("categorias").stream()  # Obtém todas as categorias
    categorias = [{**cat.to_dict(), "id": cat.id} for cat in categorias_ref]  # Converte os documentos para dicionários
    return {"categorias": categorias}

# Obter uma categoria específica pelo ID
@app.get("/categorias/{categoria_id}")
async def obter_categoria(categoria_id: str):
    """
    Busca uma categoria pelo ID.
    """
    doc_ref = db.collection("categorias").document(categoria_id)  # Referência ao documento no Firestore
    doc = doc_ref.get()
    if doc.exists:
        return {**doc.to_dict(), "id": categoria_id}
    raise HTTPException(status_code=404, detail="Categoria não encontrada")

# Atualizar uma categoria existente
@app.put("/categorias/{categoria_id}")
async def atualizar_categoria(categoria_id: str, categoria: Categoria):
    """
    Atualiza os dados de uma categoria existente.
    """
    doc_ref = db.collection("categorias").document(categoria_id)
    if not doc_ref.get().exists:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    doc_ref.update(categoria.model_dump())
    return {"mensagem": "Categoria atualizada com sucesso"}

# Deletar uma categoria pelo ID
@app.delete("/categorias/{categoria_id}")
async def deletar_categoria(categoria_id: str):
    """
    Remove uma categoria do banco de dados.
    """
    doc_ref = db.collection("categorias").document(categoria_id)
    if not doc_ref.get().exists:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    doc_ref.delete()
    return {"mensagem": "Categoria deletada com sucesso"}

# ---------------------- ROTAS PARA ITENS ----------------------

# Criar um novo item vinculado a uma categoria
@app.post("/items/")
async def criar_item(item: Item):
    """
    Cria um novo item e o vincula a uma categoria, se especificada.
    """
    if item.categoria_id:
        # Verifica se a categoria existe antes de criar o item
        cat_ref = db.collection("categorias").document(item.categoria_id)
        if not cat_ref.get().exists:
            raise HTTPException(status_code=400, detail="Categoria não encontrada")
    
    doc_ref = db.collection("items").document()
    doc_ref.set(item.dict())
    return {"id": doc_ref, "mensagem": "Item criado com sucesso"}

# Listar todos os itens cadastrados
@app.get("/items/")
async def listar_itens():
    """
    Retorna a lista de todos os itens cadastrados.
    """
    itens_ref = db.collection("items").stream()
    itens = [{**item.to_dict(), "id": item.id} for item in itens_ref]
    return {"items": itens}

# Obter um item específico pelo ID
@app.get("/items/{item_id}")
async def obter_item(item_id: str):
    """
    Busca um item específico pelo ID.
    """
    doc_ref = db.collection("items").document(item_id)
    doc = doc_ref.get()
    if doc.exists:
        return {**doc.to_dict(), "id": item_id}
    raise HTTPException(status_code=404, detail="Item não encontrado")

# Atualizar um item existente
@app.put("/items/{item_id}")
async def atualizar_item(item_id: str, item: Item):
    """
    Atualiza os dados de um item existente.
    """
    doc_ref = db.collection("items").document(item_id)
    if not doc_ref.get().exists:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    
    # Verifica se a categoria informada existe
    if item.categoria_id:
        cat_ref = db.collection("categorias").document(item.categoria_id)
        if not cat_ref.get().exists:
            raise HTTPException(status_code=400, detail="Categoria não encontrada")
    
    doc_ref.update(item.dict())
    return {"mensagem": "Item atualizado com sucesso"}

# Deletar um item pelo ID
@app.delete("/items/{item_id}")
async def deletar_item(item_id: str):
    """
    Remove um item do banco de dados.
    """
    doc_ref = db.collection("items").document(item_id)
    if not doc_ref.get().exists:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    doc_ref.delete()
    return {"mensagem": "Item deletado com sucesso"}





# ---------------------- LISTAGEM DE ITENS POR CATEGORIA ----------------------

# Listar todos os itens de uma categoria específica pelo nome da categoria
@app.get("/categorias/nome/{categoria_nome}/items/")
async def listar_itens_por_nome_categoria(categoria_nome: str):
    """
    Retorna todos os itens vinculados a uma categoria, pesquisando pelo nome da categoria.
    """
    # Busca a categoria pelo nome
    categorias_ref = db.collection("categorias").where("nome", "==", categoria_nome).stream()
    categorias = [cat for cat in categorias_ref]

    if not categorias:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")

    # Assumindo que não existam categorias com nomes duplicados, pegamos o primeiro resultado
    categoria_id = categorias[0].id

    # Busca todos os itens dessa categoria
    itens_ref = db.collection("items").where("categoria_id", "==", categoria_id).stream()
    itens = [{**item.to_dict(), "id": item.id} for item in itens_ref]

    return {"categoria_nome": categoria_nome, "categoria_id": categoria_id, "itens": itens}








