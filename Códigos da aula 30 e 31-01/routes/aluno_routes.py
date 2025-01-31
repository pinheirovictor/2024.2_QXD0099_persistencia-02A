from fastapi import APIRouter, HTTPException
from config import db
from schemas import Aluno
from typing import List, Dict, Any
from bson import ObjectId

# Criação do roteador para agrupar as rotas relacionadas aos alunos
router = APIRouter()

# Criar um novo aluno
@router.post("/", response_model=Aluno)
async def criar_aluno(aluno: Aluno):
    """
    Cria um novo aluno no banco de dados.
    """
    # Converte o objeto Pydantic para um dicionário, excluindo o ID para permitir que o MongoDB gere automaticamente
    aluno_dict = aluno.dict(by_alias=True, exclude={"id"})
    
    # Insere o aluno no banco de dados
    novo_aluno = await db.alunos.insert_one(aluno_dict)

    # Recupera o aluno recém-criado para retornar como resposta
    aluno_criado = await db.alunos.find_one({"_id": novo_aluno.inserted_id})

    # Se a criação falhar, retorna um erro
    if not aluno_criado:
        raise HTTPException(status_code=400, detail="Erro ao criar aluno")

    # Converte o `_id` do MongoDB para string antes de retornar
    aluno_criado["_id"] = str(aluno_criado["_id"])

    return aluno_criado


# Listar alunos com paginação
@router.get("/", response_model=List[Aluno])
async def listar_alunos(skip: int = 0, limit: int = 10):
    """
    Lista os alunos do banco de dados com suporte a paginação (skip e limit).
    """
    alunos = await db.alunos.find().skip(skip).limit(limit).to_list(100)

    # Converte `_id` para string antes de retornar
    for aluno in alunos:
        aluno["_id"] = str(aluno["_id"])
        
        # Converte os IDs dos cursos para string, se existirem
        if "cursos" in aluno and isinstance(aluno["cursos"], list):
            aluno["cursos"] = [str(curso_id) if isinstance(curso_id, ObjectId) else curso_id for curso_id in aluno["cursos"]]

    return alunos


# Buscar um aluno por ID
@router.get("/alunos/{aluno_id}", response_model=Aluno)
async def buscar_aluno_por_id(aluno_id: str) -> Dict[str, Any]:
    """
    Busca um aluno pelo ID fornecido.
    """
    # Verifica se o ID é válido e ajusta o filtro de busca
    filtro = {"_id": ObjectId(aluno_id)} if ObjectId.is_valid(aluno_id) else {"_id": aluno_id}

    # Procura o aluno no banco de dados
    aluno = await db.alunos.find_one(filtro)

    # Se o aluno não for encontrado, retorna erro
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    # Converte `_id` para string antes de retornar
    aluno["_id"] = str(aluno["_id"])

    # Converte os IDs dos cursos para string, se existirem
    if "cursos" in aluno and isinstance(aluno["cursos"], list):
        aluno["cursos"] = [str(curso_id) if isinstance(curso_id, ObjectId) else curso_id for curso_id in aluno["cursos"]]

    return aluno




# Atualizar dados de um aluno
@router.put("/{aluno_id}", response_model=Aluno)
async def atualizar_aluno(aluno_id: str, aluno: Aluno):
    """
    Atualiza as informações de um aluno pelo ID.
    """
    # Verifica se o ID fornecido é válido
    if not ObjectId.is_valid(aluno_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    # Converte os dados do aluno para um dicionário, excluindo o ID
    aluno_dict = aluno.model_dump(by_alias=True, exclude={"id"})
    
    # Atualiza o aluno no banco de dados
    resultado = await db.alunos.update_one({"_id": ObjectId(aluno_id)}, {"$set": aluno_dict})

    # Se nenhum documento foi modificado, significa que o aluno não existe
    if resultado.matched_count == 0:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    # Busca o aluno atualizado para retorno
    aluno_atualizado = await db.alunos.find_one({"_id": ObjectId(aluno_id)})
    aluno_atualizado["_id"] = str(aluno_atualizado["_id"])

    return aluno_atualizado


# 🔹 Excluir um aluno e removê-lo de cursos
@router.delete("/{aluno_id}", status_code=200)
async def excluir_aluno(aluno_id: str):
    """
    Exclui um aluno do banco de dados e remove sua referência dos cursos onde estava matriculado.
    """

    # Verifica se o ID é válido
    if not ObjectId.is_valid(aluno_id):
        raise HTTPException(status_code=400, detail="ID de aluno inválido")

    aluno_obj_id = ObjectId(aluno_id)

    # Verifica se o aluno existe antes de tentar excluí-lo
    aluno = await db.alunos.find_one({"_id": aluno_obj_id})
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    # Exclui o aluno do banco de dados
    delete_result = await db.alunos.delete_one({"_id": aluno_obj_id})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=500, detail="Erro ao excluir aluno")

    # 🔹 Remove o ID do aluno da lista de alunos nos cursos onde estava matriculado
    await db.cursos.update_many(
        {"alunos": aluno_obj_id},  # Filtra cursos que contêm esse aluno
        {"$pull": {"alunos": aluno_obj_id}}  # Remove o aluno da lista de `alunos`
    )

    return {"message": "Aluno excluído e removido dos cursos com sucesso"}

