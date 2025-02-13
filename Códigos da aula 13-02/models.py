from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

# ==============================
#      RELACIONAMENTO N:N
# ==============================

# Classe intermediária para o relacionamento N:N entre BensEDireitos e DividasEOnus
# Como um bem pode estar associado a múltiplas dívidas e uma dívida pode estar ligada a múltiplos bens,
# é necessário criar uma tabela auxiliar para armazenar essas associações.
class BensDividasLink(SQLModel, table=True):
    bens_id: Optional[int] = Field(default=None, foreign_key="bensedireitos.id", primary_key=True)
    divida_id: Optional[int] = Field(default=None, foreign_key="dividaseonus.id", primary_key=True)

# ==============================
#        TABELAS PRINCIPAIS
# ==============================

# Modelo para armazenar informações sobre Bens e Direitos declarados no imposto de renda
class BensEDireitos(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)  # Chave primária única para a tabela
    ano_calendario: int = Field(index=True)  # Ano de referência dos bens e direitos
    rendimentos_tributaveis: float  # Renda tributável associada aos bens
    rendimentos_isentos: float  # Renda isenta de impostos
    deducoes_previdenciarias_totais: float  # Valor deduzido para previdência
    imposto_devido: float  # Valor de imposto devido
    bens_e_direitos: float  # Valor total dos bens e direitos

    # Relacionamento 1:N com CapitalEstadoResidenciaDeclarante
    capital_estado_id: Optional[int] = Field(default=None, foreign_key="capitalestadoresidenciadeclarante.id")
    capital: Optional["CapitalEstadoResidenciaDeclarante"] = Relationship(back_populates="bens")

    # Relacionamento N:N com DividasEOnus através da tabela intermediária BensDividasLink
    dividas: List["DividasEOnus"] = Relationship(
        back_populates="bens", link_model=BensDividasLink
    )

# Modelo para representar a faixa de cálculo da base anual de imposto de renda
class FaixaBaseCalculoAnual(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)  # Identificador único da faixa de cálculo
    ano_calendario: int = Field(index=True)  # Ano de referência da base de cálculo
    tipo_declaracao: str  # Tipo de declaração (exemplo: Pessoa Física, Pessoa Jurídica)
    faixa_rendimento: str  # Faixa de renda a que se refere essa base de cálculo
    quantidade_declarantes: int  # Número de declarantes nessa faixa de rendimento
    rendimentos_tributaveis: float  # Valor total de rendimentos tributáveis
    rendimentos_isentos: float  # Valor total de rendimentos isentos
    imposto_devido: float  # Total de imposto devido nessa faixa de cálculo
    imposto_pago: float  # Total de imposto pago pelos declarantes dessa faixa

    # Relacionamento 1:1 com RendimentosIsentosNaoTributaveis
    rendimentos_isentos_id: Optional[int] = Field(default=None, foreign_key="rendimentosisentosnaotributaveis.id")

# Modelo para representar rendimentos isentos e não tributáveis no imposto de renda
class RendimentosIsentosNaoTributaveis(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)  # Identificador único do registro
    ano_calendario: int = Field(index=True)  # Ano de referência dos rendimentos
    faixa_salarios_minimos: str  # Faixa de salários mínimos correspondente
    bolsas_estudo_pesquisa: float  # Valor recebido de bolsas de estudo e pesquisa
    indenizacoes_trabalho_fgts: float  # Indenizações trabalhistas e FGTS recebidos
    ganho_capital_imoveis: float  # Ganhos de capital com imóveis
    lucros_dividendos_recebidos: float  # Lucros e dividendos recebidos de empresas
    aposentadoria_pensionistas_65_anos: float  # Rendimentos de aposentadoria para maiores de 65 anos
    transferencias_patrimoniais: float  # Transferências patrimoniais (heranças, doações)

# Modelo para representar informações de declarantes de capital por estado
class CapitalEstadoResidenciaDeclarante(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)  # Identificador único do estado
    ano_calendario: int = Field(index=True)  # Ano de referência do imposto de renda
    capital_estado: str  # Nome do estado de residência do declarante
    quantidade_declarantes: int  # Número de declarantes residentes nesse estado
    rendimentos_tributaveis: float  # Renda tributável dos declarantes no estado
    rendimentos_isentos: float  # Renda isenta dos declarantes
    imposto_devido: float  # Valor total de imposto devido
    imposto_pago: float  # Valor total de imposto pago
    bens_e_direitos: float  # Valor total dos bens e direitos declarados nesse estado

    # Relacionamento 1:N com BensEDireitos
    bens: List[BensEDireitos] = Relationship(back_populates="capital")

# Modelo para representar dívidas e ônus reais no imposto de renda
class DividasEOnus(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)  # Identificador único da dívida
    ano_calendario: int = Field(index=True)  # Ano de referência da dívida
    emprestimos_exterior: float  # Valor de empréstimos tomados no exterior
    estabelecimento_bancario_comercial: float  # Dívidas com bancos comerciais
    outras_dividas_onus_reais: float  # Outras dívidas e ônus reais
    outras_pessoas_juridicas: float  # Dívidas com outras pessoas jurídicas
    pessoas_fisicas: float  # Dívidas com pessoas físicas
    sociedade_credito_financiamento_investimento: float  # Dívidas com sociedades de crédito e financiamento
    outros: float  # Outras categorias de dívidas

    # Relacionamento N:N com BensEDireitos através da tabela intermediária BensDividasLink
    bens: List["BensEDireitos"] = Relationship(
        back_populates="dividas", link_model=BensDividasLink
    )
