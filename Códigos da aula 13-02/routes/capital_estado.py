from fastapi import APIRouter, UploadFile, HTTPException, Depends, Query
import pandas as pd
import io
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from models import CapitalEstadoResidenciaDeclarante
import unidecode
from typing import List
from sqlmodel import select

router = APIRouter()

COLUNAS_CAPITAL_ESTADO = {
    "ano_calendrio": "ano_calendario",
    "capital___estado": "capital_estado",
    "quantidade_de_declarantes": "quantidade_declarantes",
    "rendimentos_tributveis": "rendimentos_tributaveis",
    "rendimentos_isentos": "rendimentos_isentos",
    "imposto_devido": "imposto_devido",
    "imposto_pago": "imposto_pago",
    "bens_e_direitos": "bens_e_direitos"
}

def normalizar_nome_coluna(nome: str) -> str:
    nome = unidecode.unidecode(nome).lower().strip()
    nome = nome.replace(" ", "_").replace("-", "_")
    return nome

@router.post("/upload/capital-estado-residencia")
async def capital_estado_residencia(file: UploadFile, session: AsyncSession = Depends(get_session)):
    try:
        # Carregar CSV em DataFrame
        df = pd.read_csv(io.BytesIO(await file.read()))

        # Normalizar os nomes das colunas
        df.columns = [normalizar_nome_coluna(col) for col in df.columns]

        # Filtrar colunas relevantes
        colunas_para_usar = {csv_col: model_col for csv_col, model_col in COLUNAS_CAPITAL_ESTADO.items() if csv_col in df.columns}
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
        df["bens_e_direitos"] = df["bens_e_direitos"].astype(float)

        # Criar lista de objetos para inserir no banco
        registros = [CapitalEstadoResidenciaDeclarante(**row.to_dict()) for _, row in df.iterrows()]

        # Inserir no banco
        session.add_all(registros)
        await session.commit()

        return {"message": f"{len(registros)} registros inseridos em CapitalEstadoResidenciaDeclarante!"}

    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/capital-estado-residencia", response_model=List[CapitalEstadoResidenciaDeclarante])
async def get_all_capital_estado_residencia(
    session: AsyncSession = Depends(get_session),
    skip: int = Query(0, alias="offset"),
    limit: int = Query(10, alias="limit")
):
    try:
        query = select(CapitalEstadoResidenciaDeclarante).offset(skip).limit(limit)
        result = await session.execute(query)
        registros = result.scalars().all()
        return registros
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))