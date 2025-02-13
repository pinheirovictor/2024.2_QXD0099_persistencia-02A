from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

# Configuração do banco de dados PostgreSQL
DATABASE_URL = "postgresql+asyncpg://postgres:2023@localhost:5432/db2"

# Criando o motor de conexão assíncrono
engine = create_async_engine(DATABASE_URL, echo=True)

# Criando a fábrica de sessões assíncronas
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Função para criar as tabelas no banco antes de rodar a API
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

# Dependência para obter a sessão do banco
async def get_session():
    async with SessionLocal() as session:
        yield session
