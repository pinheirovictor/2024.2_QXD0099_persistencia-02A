from fastapi import APIRouter, UploadFile, HTTPException, Depends, Query
import pandas as pd
import io
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session  # Função que retorna a sessão assíncrona do banco de dados
from models import BensEDireitos  # Modelo de dados correspondente à tabela BensEDireitos
import unidecode  # Biblioteca para remover acentos e normalizar strings
from typing import List
from sqlmodel import select  # Função para criar consultas SQL

# Inicialização do roteador do FastAPI
router = APIRouter()

# Mapeamento das colunas do CSV para os atributos do modelo BensEDireitos
COLUNAS_BENS_E_DIREITOS = {
    "ano_calendario": "ano_calendario",
    "rendimentos_tributaveis": "rendimentos_tributaveis",
    "rendimentos_isentos": "rendimentos_isentos",
    "deducoes_previdenciarias_totais": "deducoes_previdenciarias_totais",
    "imposto_devido": "imposto_devido",
    "bens_e_direitos": "bens_e_direitos",
    "capital_estado_id": "capital_estado_id"
}

# Função para normalizar os nomes das colunas do CSV
def normalizar_nome_coluna(nome: str) -> str:
    """
    Normaliza o nome de uma coluna removendo acentos, 
    convertendo para minúsculas e substituindo espaços por underscores.
    """
    nome = unidecode.unidecode(nome).lower().strip()
    nome = nome.replace(" ", "_").replace("-", "_")
    return nome

# ==============================
#          ENDPOINTS
# ==============================

# Upload de CSV e inserção no banco de dados

# O arquivo CSV é lido e convertido para um DataFrame do Pandas.
# Os nomes das colunas são normalizados para evitar problemas de inconsistência.
# Apenas as colunas relevantes são utilizadas.
# Os registros são convertidos para objetos do modelo BensEDireitos e inseridos no banco.
# Consulta com paginação

# Endpoint para upload de um arquivo CSV e inserção dos dados na tabela BensEDireitos
@router.post("/upload/bens-e-direitos")
async def bens_e_direitos(file: UploadFile, session: AsyncSession = Depends(get_session)):
    """
    Recebe um arquivo CSV, processa os dados e insere os registros na tabela BensEDireitos.

    - Lê o arquivo CSV.
    - Normaliza os nomes das colunas para garantir compatibilidade.
    - Renomeia as colunas para corresponder ao modelo de dados.
    - Insere os registros na base de dados.
    """
    try:
        # Lê o arquivo CSV e converte em DataFrame do Pandas
        df = pd.read_csv(io.BytesIO(await file.read()))

        # Normaliza os nomes das colunas
        df.columns = [normalizar_nome_coluna(col) for col in df.columns]

        # Filtra apenas as colunas que existem tanto no CSV quanto no modelo
        colunas_para_usar = {csv_col: model_col for csv_col, model_col in COLUNAS_BENS_E_DIREITOS.items() if csv_col in df.columns}
        df = df.rename(columns=colunas_para_usar)[list(colunas_para_usar.values())]

        # Converte os registros do DataFrame para objetos do modelo BensEDireitos
        registros = [BensEDireitos(**row.to_dict()) for _, row in df.iterrows()]

        # Adiciona os registros à sessão e realiza o commit
        session.add_all(registros)
        await session.commit()

        return {"message": f"{len(registros)} registros inseridos em BensEDireitos!"}
    except Exception as e:
        await session.rollback()  # Em caso de erro, desfaz as alterações
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para buscar todos os registros de BensEDireitos com paginação
@router.get("/bens-e-direitos", response_model=List[BensEDireitos])
async def get_all_bens_e_direitos(
    session: AsyncSession = Depends(get_session),
    skip: int = Query(0, alias="offset"),  # Ponto inicial da consulta (default: 0)
    limit: int = Query(10, alias="limit")  # Número máximo de registros por página (default: 10)
):
    """
    Retorna uma lista de registros de BensEDireitos com suporte a paginação.

    - Utiliza `offset` e `limit` para definir a paginação.
    """
    try:
        query = select(BensEDireitos).offset(skip).limit(limit)
        result = await session.execute(query)
        registros = result.scalars().all()
        return registros
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para atualizar um registro de BensEDireitos pelo ID
@router.put("/bens-e-direitos/{id}", response_model=BensEDireitos)
async def update_bens_e_direitos(id: int, bens_direitos_update: BensEDireitos, session: AsyncSession = Depends(get_session)):
    """
    Atualiza um registro de BensEDireitos com base no ID.

    - Primeiro, busca o registro no banco de dados.
    - Se encontrado, atualiza os campos informados.
    - Faz o commit para salvar as alterações.
    """
    try:
        # Busca o registro pelo ID
        result = await session.execute(select(BensEDireitos).where(BensEDireitos.id == id))
        registro = result.scalars().first()

        # Se o registro não for encontrado, retorna erro 404
        if not registro:
            raise HTTPException(status_code=404, detail="Registro não encontrado")

        # Atualiza os atributos do objeto apenas com os valores informados na requisição
        for key, value in bens_direitos_update.dict(exclude_unset=True).items():
            setattr(registro, key, value)

        session.add(registro)
        await session.commit()
        return registro
    except Exception as e:
        await session.rollback()  # Em caso de erro, desfaz as alterações
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para deletar um registro de BensEDireitos pelo ID
@router.delete("/bens-e-direitos/{id}")
async def delete_bens_e_direitos(id: int, session: AsyncSession = Depends(get_session)):
    """
    Deleta um registro de BensEDireitos pelo ID.

    - Primeiro, verifica se o registro existe.
    - Se encontrado, remove da base de dados.
    """
    try:
        # Busca o registro pelo ID
        result = await session.execute(select(BensEDireitos).where(BensEDireitos.id == id))
        registro = result.scalars().first()

        # Se o registro não for encontrado, retorna erro 404
        if not registro:
            raise HTTPException(status_code=404, detail="Registro não encontrado")

        # Remove o registro e faz o commit
        await session.delete(registro)
        await session.commit()

        return {"message": f"Registro {id} deletado com sucesso"}
    except Exception as e:
        await session.rollback()  # Em caso de erro, desfaz as alterações
        raise HTTPException(status_code=500, detail=str(e))







# from fastapi import APIRouter, UploadFile, HTTPException, Depends, Query
# import pandas as pd
# import io
# from sqlalchemy.ext.asyncio import AsyncSession
# from database import get_session
# from models import BensEDireitos
# import unidecode
# from typing import List
# from sqlmodel import select

# router = APIRouter()

# COLUNAS_BENS_E_DIREITOS = {
#     "ano_calendario": "ano_calendario",
#     "rendimentos_tributaveis": "rendimentos_tributaveis",
#     "rendimentos_isentos": "rendimentos_isentos",
#     "deducoes_previdenciarias_totais": "deducoes_previdenciarias_totais",
#     "imposto_devido": "imposto_devido",
#     "bens_e_direitos": "bens_e_direitos",
#     "capital_estado_id": "capital_estado_id"
# }

# def normalizar_nome_coluna(nome: str) -> str:
#     nome = unidecode.unidecode(nome).lower().strip()
#     nome = nome.replace(" ", "_").replace("-", "_")
#     return nome

# @router.post("/upload/bens-e-direitos")
# async def bens_e_direitos(file: UploadFile, session: AsyncSession = Depends(get_session)):
#     try:
#         df = pd.read_csv(io.BytesIO(await file.read()))
#         df.columns = [normalizar_nome_coluna(col) for col in df.columns]
#         colunas_para_usar = {csv_col: model_col for csv_col, model_col in COLUNAS_BENS_E_DIREITOS.items() if csv_col in df.columns}
#         df = df.rename(columns=colunas_para_usar)[list(colunas_para_usar.values())]
#         registros = [BensEDireitos(**row.to_dict()) for _, row in df.iterrows()]
#         session.add_all(registros)
#         await session.commit()
#         return {"message": f"{len(registros)} registros inseridos em BensEDireitos!"}
#     except Exception as e:
#         await session.rollback()
#         raise HTTPException(status_code=500, detail=str(e))


# @router.get("/bens-e-direitos", response_model=List[BensEDireitos])
# async def get_all_bens_e_direitos(
#     session: AsyncSession = Depends(get_session),
#     skip: int = Query(0, alias="offset"),
#     limit: int = Query(10, alias="limit")
# ):
#     try:
#         query = select(BensEDireitos).offset(skip).limit(limit)
#         result = await session.execute(query)
#         registros = result.scalars().all()
#         return registros
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @router.put("/bens-e-direitos/{id}", response_model=BensEDireitos)
# async def update_bens_e_direitos(id: int, bens_direitos_update: BensEDireitos, session: AsyncSession = Depends(get_session)):
#     try:
#         result = await session.execute(select(BensEDireitos).where(BensEDireitos.id == id))
#         registro = result.scalars().first()
#         if not registro:
#             raise HTTPException(status_code=404, detail="Registro não encontrado")
        
#         for key, value in bens_direitos_update.dict(exclude_unset=True).items():
#             setattr(registro, key, value)

#         session.add(registro)
#         await session.commit()
#         return registro
#     except Exception as e:
#         await session.rollback()
#         raise HTTPException(status_code=500, detail=str(e))

# @router.delete("/bens-e-direitos/{id}")
# async def delete_bens_e_direitos(id: int, session: AsyncSession = Depends(get_session)):
#     try:
#         result = await session.execute(select(BensEDireitos).where(BensEDireitos.id == id))
#         registro = result.scalars().first()
#         if not registro:
#             raise HTTPException(status_code=404, detail="Registro não encontrado")
        
#         await session.delete(registro)
#         await session.commit()
#         return {"message": f"Registro {id} deletado com sucesso"}
#     except Exception as e:
#         await session.rollback()
#         raise HTTPException(status_code=500, detail=str(e))