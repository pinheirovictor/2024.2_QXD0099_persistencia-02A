from sqlmodel import create_engine, Session, SQLModel
from dotenv import load_dotenv
import logging
import os

# Carregar variáveis do arquivo .env
load_dotenv("db.env")

# Configurar o logger
logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

# Configuração do banco de dados
engine = create_engine(os.getenv("DATABASE_URL"))

# Criar a(s) tabela(s) no banco de dados
# Inicializa o banco de dados
def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)

def get_session() -> Session:
    return Session(engine)


