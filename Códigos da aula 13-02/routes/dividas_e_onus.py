from fastapi import APIRouter, UploadFile, HTTPException, Depends
import pandas as pd
import io
import unidecode
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from models import DividasEOnus
from typing import List
from fastapi import Query
from sqlmodel import select

router = APIRouter()

# Mapeamento das colunas do CSV para o modelo
COLUNAS_DIVIDAS_E_ONUS = {
    "ano_calendrio": "ano_calendario",
    "emprstimos_contrados_no_exterior": "emprestimos_exterior",
    "estabelecimento_bancrio_comercial": "estabelecimento_bancario_comercial",
    "outras_dvidas_e_nus_reais": "outras_dividas_onus_reais",
    "outras_pessoas_jurdicas": "outras_pessoas_juridicas",
    "pessoas_fsicas": "pessoas_fisicas",
    "soc_de_crdito_financiamento_e_investimento": "sociedade_credito_financiamento_investimento",
    "outros": "outros"
}

# Função para normalizar os nomes das colunas
def normalizar_nome_coluna(nome: str) -> str:
    nome = unidecode.unidecode(nome).lower().strip()
    nome = nome.replace(" ", "_").replace("-", "_")
    return nome

@router.post("/upload/dividas-e-onus")
async def dividas_e_onus(file: UploadFile, session: AsyncSession = Depends(get_session)):
    try:
        # Carregar CSV em DataFrame
        df = pd.read_csv(io.BytesIO(await file.read()))

        # Normalizar os nomes das colunas
        df.columns = [normalizar_nome_coluna(col) for col in df.columns]

        # Filtrar colunas relevantes
        colunas_para_usar = {csv_col: model_col for csv_col, model_col in COLUNAS_DIVIDAS_E_ONUS.items() if csv_col in df.columns}
        df = df.rename(columns=colunas_para_usar)[list(colunas_para_usar.values())]

        # Tratar valores ausentes (substituir por 0 se for numérico)
        df.fillna(0, inplace=True)

        # Conversão de tipos para evitar erros
        df["ano_calendario"] = df["ano_calendario"].astype(int)
        df["emprestimos_exterior"] = df["emprestimos_exterior"].astype(float)
        df["estabelecimento_bancario_comercial"] = df["estabelecimento_bancario_comercial"].astype(float)
        df["outras_dividas_onus_reais"] = df["outras_dividas_onus_reais"].astype(float)
        df["outras_pessoas_juridicas"] = df["outras_pessoas_juridicas"].astype(float)
        df["pessoas_fisicas"] = df["pessoas_fisicas"].astype(float)
        df["sociedade_credito_financiamento_investimento"] = df["sociedade_credito_financiamento_investimento"].astype(float)
        df["outros"] = df["outros"].astype(float)

        # Criar lista de objetos para inserir no banco
        registros = [DividasEOnus(**row.to_dict()) for _, row in df.iterrows()]

        # Inserir no banco
        session.add_all(registros)
        await session.commit()

        return {"message": f"{len(registros)} registros inseridos em DividasEOnus!"}

    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dividas-e-onus", response_model=List[DividasEOnus])
async def get_all_dividas_e_onus(
    session: AsyncSession = Depends(get_session),
    skip: int = Query(0, alias="offset"),
    limit: int = Query(10, alias="limit")
):
    try:
        query = select(DividasEOnus).offset(skip).limit(limit)
        result = await session.execute(query)
        registros = result.scalars().all()
        return registros
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))