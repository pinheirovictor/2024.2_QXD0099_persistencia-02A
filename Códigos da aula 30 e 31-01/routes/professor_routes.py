from fastapi import APIRouter, HTTPException
from config import db
from schemas import Professor
from typing import List
from bson import ObjectId

router = APIRouter()

@router.post("/", response_model=Professor)
async def criar_professor(professor: Professor):
    professor_dict = professor.dict(by_alias=True, exclude={"id"})  # Remove _id para o Mongo gerar
    novo_professor = await db.professores.insert_one(professor_dict)

    professor_criado = await db.professores.find_one({"_id": novo_professor.inserted_id})

    if not professor_criado:
        raise HTTPException(status_code=400, detail="Erro ao criar professor")

    professor_criado["_id"] = str(professor_criado["_id"])  # Converte ObjectId para string

    return professor_criado


@router.get("/", response_model=list[Professor])
async def listar_professores(skip: int = 0, limit: int = 10):
    professores = await db.professores.find().skip(skip).limit(limit).to_list(100)

    for prof in professores:
        prof["_id"] = str(prof["_id"])  # Convertendo ObjectId para string

    return professores

@router.get("/professor/{professor_id}", response_model=Professor)
async def obter_professor(professor_id: str):
    if not ObjectId.is_valid(professor_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    professor = await db.professores.find_one({"_id": ObjectId(professor_id)})

    if not professor:
        raise HTTPException(status_code=404, detail="Professor não encontrado")

    professor["_id"] = str(professor["_id"])

    return professor

@router.put("/{professor_id}", response_model=Professor)
async def atualizar_professor(professor_id: str, professor: Professor):
    if not ObjectId.is_valid(professor_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    professor_dict = professor.dict(by_alias=True, exclude={"id"})
    resultado = await db.professores.update_one({"_id": ObjectId(professor_id)}, {"$set": professor_dict})

    if resultado.matched_count == 0:
        raise HTTPException(status_code=404, detail="Professor não encontrado")

    professor_atualizado = await db.professores.find_one({"_id": ObjectId(professor_id)})
    professor_atualizado["_id"] = str(professor_atualizado["_id"])

    return professor_atualizado


@router.delete("/{professor_id}")
async def deletar_professor(professor_id: str):
    if not ObjectId.is_valid(professor_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    resultado = await db.professores.delete_one({"_id": ObjectId(professor_id)})

    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Professor não encontrado")

    return {"message": "Professor deletado com sucesso"}
