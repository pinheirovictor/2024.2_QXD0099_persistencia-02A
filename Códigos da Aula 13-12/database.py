from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from models import Base
import settings

# Configuração do banco de dados
engine = create_engine(settings.DATABASE_URL)

# Criar a(s) tabela(s) no banco de dados
Base.metadata.create_all(engine)

def get_session() -> Session:
    Session = sessionmaker(bind=engine)
    return Session()
