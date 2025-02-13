from fastapi import APIRouter, UploadFile, HTTPException, Depends
import pandas as pd
import io
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from models import RendimentosIsentosNaoTributaveis
import unidecode

from typing import List
from fastapi import Query
from sqlmodel import select


router = APIRouter()

# Mapeamento das colunas do CSV para o modelo
COLUNAS_RENDIMENTOS_ISENTOS = {
    "ano_calendrio": "ano_calendario",
    "faixa_de_salrios_mnimos": "faixa_salarios_minimos",
    "bolsas_de_estudo_e_de_pesquisa_caracterizadas_como_doao_exceto_mdico_residente_ou_pronatec_exclusivamente_para_proceder_a_estudos_ou_pesquisas_e_desde_que_os_resultados_dessas_atividades_no_representem_vantagem_para_o_doador_nem_importem_contraprestao_de_servios": "bolsas_estudo_pesquisa",
    "indenizaes_por_resciso_de_contrato_de_trabalho_inclusive_a_ttulo_de_pdv_e_por_acidente_de_trabalho_e_fgts": "indenizacoes_trabalho_fgts",
    "ganho_de_capital_na_alienao_de_bem_direito_ou_conjunto_de_bens_ou_direitos_da_mesma_natureza_alienados_em_um_mesmo_ms_de_valor_total_de_alienao_at_r_2000000_para_aes_alienadas_no_mercado_de_balco_e_r_3500000_nos_demais_casos": "ganho_capital_imoveis",
    "lucros_e_dividendos_recebidos": "lucros_dividendos_recebidos",
    "parcela_isenta_de_proventos_de_aposentadoria_reserva_remunerada_reforma_e_penso_de_declarante_com_65_anos_ou_mais": "aposentadoria_pensionistas_65_anos",
    "transferncias_patrimoniais___doaes_e_heranas": "transferencias_patrimoniais"
}

# Função para normalizar os nomes das colunas
def normalizar_nome_coluna(nome: str) -> str:
    nome = unidecode.unidecode(nome).lower().strip()
    nome = nome.replace(" ", "_").replace("-", "_")
    return nome

@router.post("/upload/rendimentos-isentos")
async def rendimentos_isentos(file: UploadFile, session: AsyncSession = Depends(get_session)):
    try:
        # Carregar CSV em DataFrame
        df = pd.read_csv(io.BytesIO(await file.read()))

        # Normalizar os nomes das colunas
        df.columns = [normalizar_nome_coluna(col) for col in df.columns]

        # Filtrar colunas relevantes
        colunas_para_usar = {csv_col: model_col for csv_col, model_col in COLUNAS_RENDIMENTOS_ISENTOS.items() if csv_col in df.columns}
        df = df.rename(columns=colunas_para_usar)[list(colunas_para_usar.values())]

        # Tratar valores ausentes (substituir por 0 se for numérico)
        df.fillna(0, inplace=True)

        # Conversão de tipos para evitar erros
        df["ano_calendario"] = df["ano_calendario"].astype(int)
        df["bolsas_estudo_pesquisa"] = df["bolsas_estudo_pesquisa"].astype(float)
        df["indenizacoes_trabalho_fgts"] = df["indenizacoes_trabalho_fgts"].astype(float)
        df["ganho_capital_imoveis"] = df["ganho_capital_imoveis"].astype(float)
        df["lucros_dividendos_recebidos"] = df["lucros_dividendos_recebidos"].astype(float)
        df["aposentadoria_pensionistas_65_anos"] = df["aposentadoria_pensionistas_65_anos"].astype(float)
        df["transferencias_patrimoniais"] = df["transferencias_patrimoniais"].astype(float)

        # Criar lista de objetos para inserir no banco
        registros = [RendimentosIsentosNaoTributaveis(**row.to_dict()) for _, row in df.iterrows()]

        # Inserir no banco
        session.add_all(registros)
        await session.commit()

        return {"message": f"{len(registros)} registros inseridos em RendimentosIsentosNaoTributaveis!"}

    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/rendimentos-isentos", response_model=List[RendimentosIsentosNaoTributaveis])
async def get_all_rendimentos_isentos(
    session: AsyncSession = Depends(get_session),
    skip: int = Query(0, alias="offset"),
    limit: int = Query(10, alias="limit")
):
    try:
        query = select(RendimentosIsentosNaoTributaveis).offset(skip).limit(limit)
        result = await session.execute(query)
        registros = result.scalars().all()
        return registros
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
