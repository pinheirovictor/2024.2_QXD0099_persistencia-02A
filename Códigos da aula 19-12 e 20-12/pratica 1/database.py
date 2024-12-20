from sqlmodel import create_engine, Session, SQLModel
from dotenv import load_dotenv
import os

# Carregar variáveis do arquivo .env
load_dotenv("db.env")

# Configuração do banco de dados
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)

# Criar tabelas no banco de dados
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session() -> Session:
    return Session(engine)
