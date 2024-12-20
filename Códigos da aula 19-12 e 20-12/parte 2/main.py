from models import Aluno
from sqlmodel import select
from database import get_session, create_db_and_tables

create_db_and_tables()

# Obter uma sessão para interagir com o banco de dados
with get_session() as session:
    # Inserir novos registros
    try:
        session.add(Aluno(nome='Maria', apelido='Mari'))
        session.add(Aluno(nome='João'))
        # Consultar registros
        alunos = session.exec(select(Aluno)).all()
        for aluno in alunos:
            print(aluno)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f'Erro: {e}')


