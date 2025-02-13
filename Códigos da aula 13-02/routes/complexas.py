from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from database import get_session  # Importa a sessão do banco de dados
from models import (
    BensEDireitos,
    FaixaBaseCalculoAnual,
    RendimentosIsentosNaoTributaveis,
    CapitalEstadoResidenciaDeclarante,
    DividasEOnus,
    BensDividasLink
)

# Inicializa o roteador para agrupar os endpoints
router = APIRouter()

# ==============================
#      CONSULTA POR ESTADO
# ==============================

@router.get("/consulta/rendimentos-por-estado")
async def consultar_rendimentos_por_estado(
    ano_calendario: int, 
    faixa_rendimento: str, 
    session: AsyncSession = Depends(get_session)
):
    """
    Consulta os rendimentos tributáveis e isentos por estado para um determinado ano e faixa de rendimento.

    - Faz um join entre `CapitalEstadoResidenciaDeclarante`, `FaixaBaseCalculoAnual` e `RendimentosIsentosNaoTributaveis`.
    - Retorna informações financeiras dos declarantes agrupadas por estado.
    """
    try:
        stmt = (
            select(
                CapitalEstadoResidenciaDeclarante.capital_estado,
                FaixaBaseCalculoAnual.rendimentos_tributaveis,
                FaixaBaseCalculoAnual.rendimentos_isentos,
                RendimentosIsentosNaoTributaveis.lucros_dividendos_recebidos,
                RendimentosIsentosNaoTributaveis.transferencias_patrimoniais
            )
            .join(FaixaBaseCalculoAnual, FaixaBaseCalculoAnual.ano_calendario == CapitalEstadoResidenciaDeclarante.ano_calendario)
            .join(RendimentosIsentosNaoTributaveis, FaixaBaseCalculoAnual.rendimentos_isentos_id == RendimentosIsentosNaoTributaveis.id)
            .where(
                FaixaBaseCalculoAnual.ano_calendario == ano_calendario,
                FaixaBaseCalculoAnual.faixa_rendimento == faixa_rendimento
            )
        )

        result = await session.execute(stmt)
        dados = result.all()

        if not dados:
            raise HTTPException(status_code=404, detail="Nenhum dado encontrado para os filtros fornecidos.")

        return [
            {
                "estado": row.capital_estado,
                "rendimentos_tributaveis": row.rendimentos_tributaveis,
                "rendimentos_isentos": row.rendimentos_isentos,
                "lucros_dividendos": row.lucros_dividendos_recebidos,
                "transferencias_patrimoniais": row.transferencias_patrimoniais
            }
            for row in dados
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==============================
#      CONSULTA COMPLETA
# ==============================

@router.get("/consulta/completa")
async def consulta_completa(
    ano_calendario: int, 
    session: AsyncSession = Depends(get_session)
):
    """
    Realiza uma consulta abrangente sobre bens, impostos, rendimentos e dívidas no ano especificado.

    - Agrupa informações de diferentes tabelas usando joins.
    - Inclui detalhes sobre bens, impostos pagos, lucros, transferências patrimoniais e dívidas.
    """
    try:
        stmt = (
            select(
                CapitalEstadoResidenciaDeclarante.capital_estado,
                BensEDireitos.bens_e_direitos,
                FaixaBaseCalculoAnual.faixa_rendimento,
                FaixaBaseCalculoAnual.imposto_pago,
                RendimentosIsentosNaoTributaveis.lucros_dividendos_recebidos,
                RendimentosIsentosNaoTributaveis.transferencias_patrimoniais,
                DividasEOnus.emprestimos_exterior,
                DividasEOnus.estabelecimento_bancario_comercial
            )
            .join(FaixaBaseCalculoAnual, FaixaBaseCalculoAnual.ano_calendario == BensEDireitos.ano_calendario)
            .join(RendimentosIsentosNaoTributaveis, FaixaBaseCalculoAnual.rendimentos_isentos_id == RendimentosIsentosNaoTributaveis.id)
            .join(CapitalEstadoResidenciaDeclarante, CapitalEstadoResidenciaDeclarante.ano_calendario == BensEDireitos.ano_calendario)
            .join(BensDividasLink, BensEDireitos.id == BensDividasLink.bens_id)
            .join(DividasEOnus, BensDividasLink.divida_id == DividasEOnus.id)
            .where(BensEDireitos.ano_calendario == ano_calendario)
        )

        result = await session.execute(stmt)
        dados = result.all()

        if not dados:
            raise HTTPException(status_code=404, detail="Nenhum dado encontrado para o ano fornecido.")

        return [
            {
                "estado": row.capital_estado,
                "total_bens": row.bens_e_direitos,
                "faixa_rendimento": row.faixa_rendimento,
                "imposto_pago": row.imposto_pago,
                "lucros_dividendos": row.lucros_dividendos_recebidos,
                "transferencias_patrimoniais": row.transferencias_patrimoniais,
                "emprestimos_exterior": row.emprestimos_exterior,
                "dividas_bancarias": row.estabelecimento_bancario_comercial
            }
            for row in dados
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==============================
#      CONSULTA PAGINADA
# ==============================

@router.get("/consulta/completa/paginada")
async def consulta_completa(
    ano_calendario: int,
    page: int = Query(1, alias="pagina", ge=1),
    page_size: int = Query(10, alias="tamanho_pagina", ge=1, le=100),
    session: AsyncSession = Depends(get_session)
):
    """
    Retorna os mesmos dados da `consulta_completa`, mas de forma paginada.

    - Permite especificar a página e o tamanho da página.
    - Retorna metadados sobre a paginação, incluindo total de páginas e registros.
    """
    try:
        offset = (page - 1) * page_size  # Calcula o deslocamento com base na página e tamanho da página

        stmt = (
            select(
                CapitalEstadoResidenciaDeclarante.capital_estado,
                BensEDireitos.bens_e_direitos,
                FaixaBaseCalculoAnual.faixa_rendimento,
                FaixaBaseCalculoAnual.imposto_pago,
                RendimentosIsentosNaoTributaveis.lucros_dividendos_recebidos,
                RendimentosIsentosNaoTributaveis.transferencias_patrimoniais,
                DividasEOnus.emprestimos_exterior,
                DividasEOnus.estabelecimento_bancario_comercial
            )
            .join(FaixaBaseCalculoAnual, FaixaBaseCalculoAnual.ano_calendario == BensEDireitos.ano_calendario)
            .join(RendimentosIsentosNaoTributaveis, FaixaBaseCalculoAnual.rendimentos_isentos_id == RendimentosIsentosNaoTributaveis.id)
            .join(CapitalEstadoResidenciaDeclarante, CapitalEstadoResidenciaDeclarante.ano_calendario == BensEDireitos.ano_calendario)
            .join(BensDividasLink, BensEDireitos.id == BensDividasLink.bens_id)
            .join(DividasEOnus, BensDividasLink.divida_id == DividasEOnus.id)
            .where(BensEDireitos.ano_calendario == ano_calendario)
            .offset(offset)
            .limit(page_size)
        )

        result = await session.execute(stmt)
        dados = result.mappings().all()

        # Contar total de registros
        count_stmt = select(BensEDireitos.id).where(BensEDireitos.ano_calendario == ano_calendario)
        total_result = await session.execute(count_stmt)
        total_registros = len(total_result.fetchall())

        return {
            "pagina_atual": page,
            "tamanho_pagina": page_size,
            "total_registros": total_registros,
            "total_paginas": (total_registros // page_size) + (1 if total_registros % page_size > 0 else 0),
            "dados": dados
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


