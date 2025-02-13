from fastapi import APIRouter, UploadFile, HTTPException, Depends, Query
import pandas as pd
import io
import unidecode
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from models import BensDividasLink  
from sqlmodel import select
from typing import List

router = APIRouter()

# Mapeamento das colunas do CSV para o modelo
COLUNAS_BENS_DIVIDAS = {
    "bens_id": "bens_id",
    "divida_id": "divida_id"
}

# Função para normalizar os nomes das colunas
def normalizar_nome_coluna(nome: str) -> str:
    nome = unidecode.unidecode(nome).lower().strip()
    nome = nome.replace(" ", "_").replace("-", "_")
    return nome

@router.post("/upload/bens-dividas")
async def upload_bens_dividas(file: UploadFile, session: AsyncSession = Depends(get_session)):
    try:
        # Carregar CSV em DataFrame
        df = pd.read_csv(io.BytesIO(await file.read()))

        # Normalizar os nomes das colunas
        df.columns = [normalizar_nome_coluna(col) for col in df.columns]

        # Filtrar colunas relevantes
        colunas_para_usar = {csv_col: model_col for csv_col, model_col in COLUNAS_BENS_DIVIDAS.items() if csv_col in df.columns}
        df = df.rename(columns=colunas_para_usar)[list(colunas_para_usar.values())]

        # Verificar se os IDs são inteiros
        df["bens_id"] = df["bens_id"].astype(int)
        df["divida_id"] = df["divida_id"].astype(int)

        # Criar lista de objetos para inserir no banco
        registros = [BensDividasLink(**row.to_dict()) for _, row in df.iterrows()]

        # Inserir no banco
        session.add_all(registros)
        await session.commit()

        return {"message": f"{len(registros)} registros inseridos em bensdividaslink!"}

    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/bens-dividas", response_model=List[BensDividasLink])
async def get_all_bens_dividas(
    session: AsyncSession = Depends(get_session),
    skip: int = Query(0, alias="offset"),
    limit: int = Query(10, alias="limit")
):
    try:
        query = select(BensDividasLink).offset(skip).limit(limit)
        result = await session.execute(query)
        registros = result.scalars().all()
        return registros
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))