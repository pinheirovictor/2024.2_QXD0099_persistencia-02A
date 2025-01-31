from fastapi import APIRouter, HTTPException
from config import db
from schemas import Turma
from typing import List
from bson import ObjectId

router = APIRouter()

@router.post("/", response_model=Turma)
async def criar_turma(turma: Turma):
    turma_dict = turma.dict(by_alias=True, exclude={"id"})  # Excluindo _id para que o Mongo gere um
    nova_turma = await db.turmas.insert_one(turma_dict)
    
    # Buscar o documento recém-criado
    turma_criada = await db.turmas.find_one({"_id": nova_turma.inserted_id})

    if not turma_criada:
        raise HTTPException(status_code=400, detail="Erro ao criar turma")

    # Convertendo ObjectId para string antes de retornar
    turma_criada["_id"] = str(turma_criada["_id"])

    return turma_criada

@router.get("/", response_model=list[Turma])
async def listar_turmas(skip: int = 0, limit: int = 10):
    turmas = await db.turmas.find().skip(skip).limit(limit).to_list(100)

    for turma in turmas:
        turma["_id"] = str(turma["_id"])  # Convertendo ObjectId para string

    return turmas


@router.get("/turma/{turma_id}", response_model=Turma)
async def obter_turma(turma_id: str):
    if not ObjectId.is_valid(turma_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    turma = await db.turmas.find_one({"_id": ObjectId(turma_id)})

    if not turma:
        raise HTTPException(status_code=404, detail="Turma não encontrada")

    turma["_id"] = str(turma["_id"])

    return turma


@router.put("/{turma_id}", response_model=Turma)
async def atualizar_turma(turma_id: str, turma: Turma):
    if not ObjectId.is_valid(turma_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    turma_dict = turma.dict(by_alias=True, exclude={"id"})
    resultado = await db.turmas.update_one({"_id": ObjectId(turma_id)}, {"$set": turma_dict})

    if resultado.matched_count == 0:
        raise HTTPException(status_code=404, detail="Turma não encontrada")

    turma_atualizada = await db.turmas.find_one({"_id": ObjectId(turma_id)})
    turma_atualizada["_id"] = str(turma_atualizada["_id"])

    return turma_atualizada

@router.delete("/{turma_id}")
async def deletar_turma(turma_id: str):
    if not ObjectId.is_valid(turma_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    resultado = await db.turmas.delete_one({"_id": ObjectId(turma_id)})

    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Turma não encontrada")

    return {"message": "Turma deletada com sucesso"}
