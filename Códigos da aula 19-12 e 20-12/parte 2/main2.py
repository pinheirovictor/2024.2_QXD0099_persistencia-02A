from fastapi import FastAPI, Depends, HTTPException
from datetime import datetime
from sqlmodel import SQLModel, Field, select, Session
from contextlib import asynccontextmanager
from database import create_db_and_tables, get_session
from models import Aluno
from sqlalchemy.exc import SQLAlchemyError

# Configuração do ciclo de vida da aplicação
# O método lifespan é executado quando a aplicação inicia e finaliza.
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()  # Cria as tabelas no banco de dados durante a inicialização
    yield  # Mantém a aplicação ativa até ser encerrada

# Inicialização da aplicação FastAPI
app = FastAPI(lifespan=lifespan)

# Rota inicial de boas-vindas
@app.get("/")
def home():
    return {"msg": "Olá, mundo!"}  # Mensagem simples para verificar se a API está funcionando

# Rota para inserir um novo aluno
@app.post("/alunos", response_model=Aluno)
def inserir_aluno(aluno: Aluno, session: Session = Depends(get_session)) -> Aluno:
    """
    Insere um novo aluno no banco de dados.
    """
    try:
        session.add(aluno)  # Adiciona o objeto aluno à sessão
        session.commit()  # Persiste os dados no banco
        session.refresh(aluno)  # Atualiza o objeto com os dados persistidos
        return aluno  # Retorna o aluno recém-adicionado
    except SQLAlchemyError as e:
        session.rollback()  # Reverte mudanças no caso de erro
        raise HTTPException(status_code=500, detail=f"Erro ao inserir o aluno: {str(e)}")

# Rota para listar todos os alunos
@app.get("/alunos", response_model=list[Aluno])
def listar_alunos(session: Session = Depends(get_session)) -> list[Aluno]:
    """
    Lista todos os alunos do banco de dados.
    """
    try:
        alunos = session.exec(select(Aluno)).all()  # Executa a consulta para obter todos os alunos
        return alunos  # Retorna a lista de alunos
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar os alunos: {str(e)}")

# Rota para buscar um aluno pelo ID
@app.get("/alunos/{aluno_id}", response_model=Aluno)
def buscar_aluno_por_id(aluno_id: int, session: Session = Depends(get_session)) -> Aluno:
    """
    Busca um aluno específico pelo ID.
    """
    try:
        aluno = session.get(Aluno, aluno_id)  # Busca o aluno pelo ID
        if not aluno:
            raise HTTPException(status_code=404, detail="Aluno não encontrado.")  # Retorna erro 404 se não encontrar
        return aluno  # Retorna o aluno encontrado
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar o aluno: {str(e)}")

# Rota para atualizar os dados de um aluno
@app.put("/alunos/{aluno_id}", response_model=Aluno)
def atualizar_aluno(aluno_id: int, aluno: Aluno, session: Session = Depends(get_session)) -> Aluno:
    """
    Atualiza as informações de um aluno existente.
    """
    try:
        aluno_existente = session.get(Aluno, aluno_id)  # Verifica se o aluno existe
        if not aluno_existente:
            raise HTTPException(status_code=404, detail="Aluno não encontrado.")  # Retorna erro 404 se não existir
        
        # Atualiza os campos do aluno existente com os valores fornecidos
        for key, value in aluno.dict(exclude_unset=True).items():
            setattr(aluno_existente, key, value)
        
        session.add(aluno_existente)  # Adiciona o objeto atualizado à sessão
        session.commit()  # Persiste as alterações no banco
        session.refresh(aluno_existente)  # Atualiza o objeto com os dados persistidos
        return aluno_existente  # Retorna o aluno atualizado
    except SQLAlchemyError as e:
        session.rollback()  # Reverte mudanças no caso de erro
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar o aluno: {str(e)}")

# Rota para excluir um aluno
@app.delete("/alunos/{aluno_id}", response_model=dict)
def deletar_aluno(aluno_id: int, session: Session = Depends(get_session)) -> dict:
    """
    Exclui um aluno do banco de dados.
    """
    try:
        aluno = session.get(Aluno, aluno_id)  # Verifica se o aluno existe
        if not aluno:
            raise HTTPException(status_code=404, detail="Aluno não encontrado.")  # Retorna erro 404 se não existir
        
        session.delete(aluno)  # Remove o aluno da sessão
        session.commit()  # Persiste a exclusão no banco
        return {"msg": "Aluno excluído com sucesso."}  # Retorna mensagem de confirmação
    except SQLAlchemyError as e:
        session.rollback()  # Reverte mudanças no caso de erro
        raise HTTPException(status_code=500, detail=f"Erro ao excluir o aluno: {str(e)}")
