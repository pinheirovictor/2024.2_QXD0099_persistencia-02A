from fastapi import APIRouter, HTTPException
from config import db
from schemas import Departamento
from typing import List
from bson import ObjectId

router = APIRouter()

@router.post("/", response_model=Departamento)
async def criar_departamento(departamento: Departamento):
    # Inserindo sem _id para deixar o MongoDB gerar automaticamente
    departamento_dict = departamento.dict(by_alias=True, exclude={"id"})
    novo_departamento = await db.departamentos.insert_one(departamento_dict)
    
    # Buscando o documento recém-criado
    departamento_criado = await db.departamentos.find_one({"_id": novo_departamento.inserted_id})

    if not departamento_criado:
        raise HTTPException(status_code=400, detail="Erro ao criar departamento")

    # Convertendo ObjectId para string antes de retornar
    departamento_criado["_id"] = str(departamento_criado["_id"])

    return departamento_criado





@router.get("/", response_model=list[Departamento])
async def listar_departamentos(skip: int = 0, limit: int = 10):
    departamentos = await db.departamentos.find().skip(skip).limit(limit).to_list(100)

    for dep in departamentos:
        dep["_id"] = str(dep["_id"])  # Convertendo ObjectId para string

    return departamentos


@router.get("/departamento/{departamento_id}", response_model=Departamento)
async def obter_departamento(departamento_id: str):
    if not ObjectId.is_valid(departamento_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    departamento = await db.departamentos.find_one({"_id": ObjectId(departamento_id)})

    if not departamento:
        raise HTTPException(status_code=404, detail="Departamento não encontrado")

    departamento["_id"] = str(departamento["_id"])

    return departamento


@router.put("/{departamento_id}", response_model=Departamento)
async def atualizar_departamento(departamento_id: str, departamento: Departamento):
    if not ObjectId.is_valid(departamento_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    departamento_dict = departamento.dict(by_alias=True, exclude={"id"})
    resultado = await db.departamentos.update_one({"_id": ObjectId(departamento_id)}, {"$set": departamento_dict})

    if resultado.matched_count == 0:
        raise HTTPException(status_code=404, detail="Departamento não encontrado")

    departamento_atualizado = await db.departamentos.find_one({"_id": ObjectId(departamento_id)})
    departamento_atualizado["_id"] = str(departamento_atualizado["_id"])

    return departamento_atualizado


@router.delete("/{departamento_id}")
async def deletar_departamento(departamento_id: str):
    if not ObjectId.is_valid(departamento_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    resultado = await db.departamentos.delete_one({"_id": ObjectId(departamento_id)})

    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Departamento não encontrado")

    return {"message": "Departamento deletado com sucesso"}
