from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Aluno
from database import get_session

# Obter uma sessão para interagir com o banco de dados
session = get_session()

# Inserir novos registros
try:
    session.add(Aluno(nome='Maria', apelido='Mari'))
    session.add(Aluno(nome='João'))
    session.commit()
except Exception as e:
    session.rollback()
    print(f'Erro: {e}')

# Consultar registros
alunos = session.query(Aluno).all()
for aluno in alunos:
    print(aluno)
