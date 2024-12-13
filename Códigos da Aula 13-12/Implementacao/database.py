from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

DATABASE_URL = "sqlite:///./escola.db"

# Criar o motor do banco de dados
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Criar as tabelas
Base.metadata.create_all(bind=engine)

# Configuração da Sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependência para obter a sessão
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
