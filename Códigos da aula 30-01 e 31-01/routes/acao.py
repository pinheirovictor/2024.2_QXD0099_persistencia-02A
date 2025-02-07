from fastapi import APIRouter, HTTPException
from bson import ObjectId
from config import db
from schemas import Aluno
from typing import List
from typing import Dict, Any

router = APIRouter()

from fastapi import APIRouter, HTTPException
from bson import ObjectId
from config import db
from schemas import Aluno, Curso
from typing import List
from typing import Dict, Any

router = APIRouter()

# Rota para matricular um aluno em um curso
@router.post("/matriculas/")
async def matricular_aluno(curso_id: str, aluno_id: str):
    """
    Matricula um aluno em um curso, garantindo a consistência dos dados
    nos documentos de `cursos` e `alunos` no banco de dados MongoDB.
    """

    # Validação dos IDs fornecidos
    if not ObjectId.is_valid(curso_id) or not ObjectId.is_valid(aluno_id):
        raise HTTPException(status_code=400, detail="ID de curso ou aluno inválido")

    # Busca o curso no banco de dados
    curso = await db.cursos.find_one({"_id": ObjectId(curso_id)})
    if not curso:
        raise HTTPException(status_code=404, detail="Curso não encontrado")

    # Busca o aluno no banco de dados
    aluno = await db.alunos.find_one({"_id": ObjectId(aluno_id)})
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    # Atualiza o curso para incluir o aluno na lista de matriculados
    await db.cursos.update_one(
        {"_id": ObjectId(curso_id)},
        {"$addToSet": {"alunos": ObjectId(aluno_id)}}  # `$addToSet` impede duplicatas
    )

    # Atualiza o aluno para incluir o curso na lista de matrículas
    await db.alunos.update_one(
        {"_id": ObjectId(aluno_id)},
        {"$addToSet": {"cursos": ObjectId(curso_id)}}  # Mantém a relação N:N entre alunos e cursos
    )

    return {"message": "Aluno matriculado com sucesso!"}






@router.get("/cursos/{curso_id}/alunos")
async def alunos_por_curso(curso_id: str) -> Dict[str, Any]:
    # Verifica se o ID é válido
    if not ObjectId.is_valid(curso_id):
        raise HTTPException(status_code=400, detail="ID de curso inválido")

    # Busca o curso no banco
    curso = await db.cursos.find_one({"_id": ObjectId(curso_id)})
    if not curso:
        raise HTTPException(status_code=404, detail="Curso não encontrado")

    # Converter IDs de alunos dentro do curso para ObjectId
    if "alunos" in curso and isinstance(curso["alunos"], list):
        curso["alunos"] = [ObjectId(aluno_id) if isinstance(aluno_id, str) else aluno_id for aluno_id in curso["alunos"]]

    # Pipeline para buscar os detalhes completos dos alunos
    pipeline = [
        {"$match": {"_id": ObjectId(curso_id)}},
        {
            "$lookup": {
                "from": "alunos",  # Coleção de alunos
                "localField": "alunos",  # Lista de IDs dos alunos dentro do curso
                "foreignField": "_id",  # Campo `_id` correspondente nos alunos
                "as": "alunos_info"  # Nome do campo na resposta
            }
        },
        {"$project": {"_id": 1, "nome": 1, "descricao": 1, "carga_horaria": 1, "professor_id": 1, "alunos": "$alunos_info"}}
    ]

    resultado = await db.cursos.aggregate(pipeline).to_list(1)

    if not resultado:
        raise HTTPException(status_code=404, detail="Nenhum aluno encontrado para este curso")

    curso_detalhado = resultado[0]

    # Convertendo `_id` do curso para string
    curso_detalhado["_id"] = str(curso_detalhado["_id"])

    # Verifica se existem alunos e converte `_id` deles para string
    if "alunos" in curso_detalhado and isinstance(curso_detalhado["alunos"], list):
        for aluno in curso_detalhado["alunos"]:
            if "_id" in aluno and isinstance(aluno["_id"], ObjectId):
                aluno["_id"] = str(aluno["_id"])
            # Converte cursos dentro do aluno (se existirem)
            if "cursos" in aluno and isinstance(aluno["cursos"], list):
                aluno["cursos"] = [str(curso) if isinstance(curso, ObjectId) else curso for curso in aluno["cursos"]]

    return curso_detalhado  # Retorna apenas o curso encontrado com os alunos detalhados






@router.get("/cursos/sem_alunos", response_model=List[Curso])
async def cursos_sem_alunos():
    cursos = await db.cursos.find({"alunos": {"$size": 0}}).to_list(100)
    for curso in cursos:
        curso["_id"] = str(curso["_id"])
    return cursos


@router.get("/professores/mais_cursos/{quantidade}")
async def professores_com_mais_cursos(quantidade: int):
    pipeline = [
        {"$group": {"_id": "$professor_id", "total_cursos": {"$sum": 1}}},  # Conta cursos por professor
        {"$match": {"total_cursos": {"$gte": quantidade}}},  # Filtra professores com mais de X cursos
        {"$sort": {"total_cursos": -1}}  # Ordena
    ]
    resultado = await db.cursos.aggregate(pipeline).to_list(100)
    return resultado



@router.get("/cursos/maior_carga_horaria", response_model=List[Curso])
async def cursos_maior_carga_horaria():
    cursos = await db.cursos.find().sort("carga_horaria", -1).to_list(10)
    
    for curso in cursos:
        curso["_id"] = str(curso["_id"])  # Convertendo o _id do curso para string

        # Verifica se há alunos e converte os ObjectId da lista de alunos para strings
        if "alunos" in curso and isinstance(curso["alunos"], list):
            curso["alunos"] = [str(aluno_id) if isinstance(aluno_id, ObjectId) else aluno_id for aluno_id in curso["alunos"]]
    
    return cursos  # Retorna os cursos com carga horária ordenados corretamente



@router.get("/alunos/mais_velhos", response_model=List[Aluno])
async def alunos_mais_velhos():
    alunos = await db.alunos.find().sort("idade", -1).to_list(10)
    for aluno in alunos:
        aluno["_id"] = str(aluno["_id"])
    return alunos


# Cursos, Alunos e Professores
# Descrição: Retorna os cursos junto com os detalhes dos professores e a contagem de alunos matriculados.
@router.get("/cursos/detalhes")
async def cursos_com_professores_e_contagem_alunos():
    pipeline = [
        {
            "$lookup": {
                "from": "professores",
                "localField": "professor_id",
                "foreignField": "_id",
                "as": "professor_info"
            }
        },
        {"$unwind": {"path": "$professor_info", "preserveNullAndEmptyArrays": True}},
        {
            "$lookup": {
                "from": "alunos",
                "localField": "alunos",
                "foreignField": "_id",
                "as": "alunos_info"
            }
        },
        {
            "$addFields": {
                "total_alunos": {"$size": "$alunos_info"}
            }
        },
        {
            "$project": {
                "_id": 1,
                "nome": 1,
                "descricao": 1,
                "professor": "$professor_info.nome",
                "total_alunos": 1
            }
        }
    ]
    
    resultado = await db.cursos.aggregate(pipeline).to_list(100)
    
    for curso in resultado:
        curso["_id"] = str(curso["_id"])
    
    return resultado

# Alunos, Cursos e Departamentos
# Descrição: Retorna os alunos e os cursos que eles estão matriculados, juntamente com os departamentos responsáveis pelos cursos.
@router.get("/alunos/detalhes")
async def alunos_com_cursos_e_departamentos():
    pipeline = [
        {
            "$lookup": {
                "from": "cursos",
                "localField": "cursos",
                "foreignField": "_id",
                "as": "cursos_info"
            }
        },
        {
            "$lookup": {
                "from": "departamentos",
                "localField": "cursos_info.departamento_id",
                "foreignField": "_id",
                "as": "departamentos_info"
            }
        },
        {
            "$project": {
                "_id": 1,
                "nome": 1,
                "email": 1,
                "cursos": {
                    "$map": {
                        "input": "$cursos_info",
                        "as": "curso",
                        "in": {
                            "nome": "$$curso.nome",
                            "departamento": {
                                "$arrayElemAt": [
                                    {
                                        "$filter": {
                                            "input": "$departamentos_info",
                                            "as": "departamento",
                                            "cond": {"$eq": ["$$departamento._id", "$$curso.departamento_id"]}
                                        }
                                    },
                                    0
                                ]
                            }
                        }
                    }
                }
            }
        }
    ]

    resultado = await db.alunos.aggregate(pipeline).to_list(100)

    for aluno in resultado:
        aluno["_id"] = str(aluno["_id"])

    return resultado

# Professores, Cursos e Alunos
# Descrição: Retorna os professores, seus cursos e o total de alunos matriculados em cada curso.
@router.get("/professores/detalhes")
async def professores_com_cursos_e_total_alunos():
    pipeline = [
        {
            "$lookup": {
                "from": "cursos",
                "localField": "_id",
                "foreignField": "professor_id",
                "as": "cursos_info"
            }
        },
        {
            "$lookup": {
                "from": "alunos",
                "localField": "cursos_info._id",
                "foreignField": "cursos",
                "as": "alunos_info"
            }
        },
        {
            "$addFields": {
                "total_alunos": {"$size": "$alunos_info"}
            }
        },
        {
            "$project": {
                "_id": 1,
                "nome": 1,
                "email": 1,
                "cursos": "$cursos_info.nome",
                "total_alunos": 1
            }
        }
    ]
    
    resultado = await db.professores.aggregate(pipeline).to_list(100)
    
    for professor in resultado:
        professor["_id"] = str(professor["_id"])
    
    return resultado

# Média de Idade dos Alunos por Curso e Departamento
# Descrição: Retorna a média de idade dos alunos por curso e por departamento.

@router.get("/estatisticas/media_idade")
async def media_idade_alunos_por_curso_departamento():
    pipeline = [
        {
            "$lookup": {
                "from": "cursos",
                "localField": "cursos",
                "foreignField": "_id",
                "as": "cursos_info"
            }
        },
        {"$unwind": "$cursos_info"},
        {
            "$lookup": {
                "from": "departamentos",
                "localField": "cursos_info.departamento_id",
                "foreignField": "_id",
                "as": "departamento_info"
            }
        },
        {"$unwind": "$departamento_info"},
        {
            "$group": {
                "_id": {"curso": "$cursos_info.nome", "departamento": "$departamento_info.nome"},
                "media_idade": {"$avg": "$idade"},
                "total_alunos": {"$sum": 1}
            }
        },
        {"$sort": {"_id.departamento": 1, "media_idade": -1}}
    ]

    resultado = await db.alunos.aggregate(pipeline).to_list(100)

    return resultado
