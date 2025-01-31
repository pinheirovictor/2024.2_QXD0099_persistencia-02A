from fastapi import APIRouter, HTTPException, Query
from config import db
from schemas import Curso
from typing import List
from bson import ObjectId
from typing import Dict, Any

router = APIRouter()

@router.post("/", response_model=Curso)
async def criar_curso(curso: Curso):
    curso_dict = curso.dict(by_alias=True, exclude={"id"})  # Remove o id para o Mongo gerar um novo
    novo_curso = await db.cursos.insert_one(curso_dict)

    curso_criado = await db.cursos.find_one({"_id": novo_curso.inserted_id})

    if not curso_criado:
        raise HTTPException(status_code=400, detail="Erro ao criar curso")

    curso_criado["_id"] = str(curso_criado["_id"])  # Converte ObjectId para string antes de retornar

    return curso_criado


@router.get("/", response_model=List[Curso])
async def listar_cursos(skip: int = 0, limit: int = 10):
    cursos = await db.cursos.find().skip(skip).limit(limit).to_list(100)

    # Convertendo ObjectId para string antes de passar ao Pydantic
    for curso in cursos:
        curso["_id"] = str(curso["_id"])  # Convertendo _id do curso para string

        # Verifica se existe a chave "alunos" e converte os IDs dentro dela
        if "alunos" in curso and isinstance(curso["alunos"], list):
            curso["alunos"] = [str(aluno_id) if isinstance(aluno_id, ObjectId) else aluno_id for aluno_id in curso["alunos"]]

    return cursos  # Agora o retorno está no formato correto para FastAPI/Pydantic



@router.get("/cursos/{curso_id}", response_model=Curso)
async def buscar_curso_por_id(curso_id: str) -> Dict[str, Any]:
    """
    Busca um curso pelo ID, suportando tanto `ObjectId` quanto `string`.
    """
    # Verifica se o ID é um ObjectId válido e ajusta o filtro
    filtro = {"_id": ObjectId(curso_id)} if ObjectId.is_valid(curso_id) else {"_id": curso_id}

    # Busca o curso no banco de dados
    curso = await db.cursos.find_one(filtro)

    # Se o curso não for encontrado, retorna erro
    if not curso:
        raise HTTPException(status_code=404, detail="Curso não encontrado")

    # Convertendo `_id` para string antes de retornar
    curso["_id"] = str(curso["_id"])

    #  Convertendo a lista `alunos` para string se existir
    if "alunos" in curso and isinstance(curso["alunos"], list):
        curso["alunos"] = [str(aluno_id) if isinstance(aluno_id, ObjectId) else aluno_id for aluno_id in curso["alunos"]]

    return curso


@router.put("/{curso_id}", response_model=Curso)
async def atualizar_curso(curso_id: str, curso: Curso):
    # Verificar se o curso_id é válido antes de usar
    if not ObjectId.is_valid(curso_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    # Removendo o campo id antes da atualização para evitar erro
    curso_dict = curso.dict(by_alias=True, exclude={"id"})

    # Atualizar curso
    resultado = await db.cursos.update_one({"_id": ObjectId(curso_id)}, {"$set": curso_dict})

    # Se não encontrou e atualizou nada, retornar erro
    if resultado.matched_count == 0:
        raise HTTPException(status_code=404, detail="Curso não encontrado")

    # Buscar o curso atualizado
    curso_atualizado = await db.cursos.find_one({"_id": ObjectId(curso_id)})

    # Converter ObjectId para string antes de retornar
    curso_atualizado["_id"] = str(curso_atualizado["_id"])

    return curso_atualizado


@router.delete("/{curso_id}")
async def deletar_curso(curso_id: str):
    # Verifica se o ID é válido antes de tentar deletar
    if not ObjectId.is_valid(curso_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    # Converte o ID para ObjectId e deleta o curso
    resultado = await db.cursos.delete_one({"_id": ObjectId(curso_id)})

    # Se nenhum documento foi deletado, retorna erro 404
    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Curso não encontrado")

    return {"message": "Curso deletado com sucesso"}





@router.get("/estatisticas/alunos_por_curso")
async def alunos_por_curso():
    pipeline = [
        {"$project": {"nome": 1, "total_alunos": {"$size": "$alunos"}}},  # Conta quantos alunos tem
        {"$sort": {"total_alunos": -1}}  # Ordena do maior para o menor
    ]
    
    resultado = await db.cursos.aggregate(pipeline).to_list(100)

    # Convertendo _id para string antes de retornar
    for curso in resultado:
        curso["_id"] = str(curso["_id"])
    
    return resultado



@router.get("/buscar/{nome}", response_model=List[Curso])
async def buscar_curso(nome: str):
    cursos = await db.cursos.find({"nome": {"$regex": nome, "$options": "i"}}).to_list(100)
    
    # Convertendo _id para string antes de passar ao Pydantic
    for curso in cursos:
        curso["_id"] = str(curso["_id"])

    return cursos