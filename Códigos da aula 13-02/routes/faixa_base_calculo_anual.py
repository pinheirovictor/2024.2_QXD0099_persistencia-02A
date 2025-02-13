from fastapi import APIRouter, UploadFile, HTTPException, Depends
import pandas as pd
import io
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from models import FaixaBaseCalculoAnual
import unidecode
from typing import List
from fastapi import Query
from sqlmodel import select



router = APIRouter()

COLUNAS_FAIXA_BASE = {
    "ano_calendrio": "ano_calendario",
    "tipo_de_formulrio": "tipo_declaracao",
    "faixa_de_rendimento": "faixa_rendimento",
    "quantidade_de_declarantes": "quantidade_declarantes",
    "rendimentos_tributveis": "rendimentos_tributaveis",
    "rendimentos_isentos": "rendimentos_isentos",
    "imposto_devido": "imposto_devido",
    "imposto_pago": "imposto_pago",
    "rendimentos_isentos_id": "rendimentos_isentos_id"
}

def normalizar_nome_coluna(nome: str) -> str:
    nome = unidecode.unidecode(nome).lower().strip()
    nome = nome.replace(" ", "_").replace("-", "_")
    return nome

@router.post("/upload/faixa-base-calculo-anual")
async def faixa_base_calculo_anual(file: UploadFile, session: AsyncSession = Depends(get_session)):
    try:
        # Carregar CSV em DataFrame
        df = pd.read_csv(io.BytesIO(await file.read()))

        # Normalizar os nomes das colunas
        df.columns = [normalizar_nome_coluna(col) for col in df.columns]

        # Filtrar colunas relevantes
        colunas_para_usar = {csv_col: model_col for csv_col, model_col in COLUNAS_FAIXA_BASE.items() if csv_col in df.columns}
        df = df.rename(columns=colunas_para_usar)[list(colunas_para_usar.values())]

        # Tratar valores ausentes (substituir por 0 se for numérico)
        df.fillna(0, inplace=True)

        # Conversão de tipos para evitar erros
        df["ano_calendario"] = df["ano_calendario"].astype(int)
        df["quantidade_declarantes"] = df["quantidade_declarantes"].astype(int)
        df["rendimentos_tributaveis"] = df["rendimentos_tributaveis"].astype(float)
        df["rendimentos_isentos"] = df["rendimentos_isentos"].astype(float)
        df["imposto_devido"] = df["imposto_devido"].astype(float)
        df["imposto_pago"] = df["imposto_pago"].astype(float)
        df["rendimentos_isentos_id"] = df["rendimentos_isentos_id"].astype(int)

        # Criar lista de objetos para inserir no banco
        registros = [FaixaBaseCalculoAnual(**row.to_dict()) for _, row in df.iterrows()]

        # Inserir no banco
        session.add_all(registros)
        await session.commit()

        return {"message": f"{len(registros)} registros inseridos em FaixaBaseCalculoAnual!"}

    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))



@router.get("/faixa-base-calculo-anual", response_model=List[FaixaBaseCalculoAnual])
async def get_all_faixa_base_calculo_anual(
    session: AsyncSession = Depends(get_session),
    skip: int = Query(0, alias="offset"),
    limit: int = Query(10, alias="limit")
):
    try:
        query = select(FaixaBaseCalculoAnual).offset(skip).limit(limit)
        result = await session.execute(query)
        registros = result.scalars().all()
        return registros
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
