from fastapi import FastAPI, HTTPException, Query, Depends
from sqlalchemy import func
from sqlmodel import SQLModel, Session, create_engine, select
from typing import List, Optional, Dict, Any
from models import Membro  # Importa o modelo Membro que representa a tabela no banco de dados

# Inicializa a aplicação FastAPI
app = FastAPI()

# URL do banco de dados SQLite
DATABASE_URL = "sqlite:///database.db"
engine = create_engine(DATABASE_URL, echo=True)  # Cria o engine com logs habilitados

# Função executada no startup da aplicação para criar as tabelas no banco de dados
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)  # Cria as tabelas no banco de dados se não existirem

# Gerenciamento de sessões do banco de dados
# Gera uma sessão para cada requisição, garantindo que a conexão seja fechada após o uso
def get_session():
    with Session(engine) as session:
        yield session

# Endpoint para criar um novo membro no banco de dados
@app.post("/membros/", response_model=Membro)
def create_membro(membro: Membro, session: Session = Depends(get_session)):
    session.add(membro)  # Adiciona o novo membro à sessão
    session.commit()  # Persiste a transação no banco
    session.refresh(membro)  # Atualiza o objeto com o ID gerado no banco
    return membro  # Retorna o membro criado

# Endpoint para listar membros com paginação simples
@app.get("/membros/", response_model=List[Membro])
def read_membros(
    last_id: Optional[int] = Query(None),  # ID do último membro exibido (para paginação)
    page_size: int = Query(10),  # Tamanho da página, valor padrão = 10
    session: Session = Depends(get_session)
):
    if last_id:  # Consulta membros com base no ID do último membro
        query = select(Membro).where(Membro.id > last_id).limit(page_size)
    else:
        query = select(Membro).limit(page_size)  # Retorna os primeiros membros se last_id não for fornecido
    membros = session.exec(query).all()  # Executa a consulta e retorna os resultados
    return membros


# Endpoint para listar membros com paginação detalhada (offset/limit)
@app.get("/membros/paginados/", response_model=Dict[str, Any])
def read_membros_paginated(
    offset: int = Query(0, ge=0),  # Define o ponto inicial da consulta
    limit: int = Query(10, ge=1),  # Limita o número de resultados por página
    session: Session = Depends(get_session)
):
    total = session.exec(select(func.count(Membro.id))).one_or_none() or (0)  # Obtém o total de membros
    membros = session.exec(select(Membro).offset(offset).limit(limit)).all()  # Consulta membros com offset/limit
    current_page = (offset // limit) + 1  # Calcula a página atual
    total_pages = (total // limit) + (1 if total % limit > 0 else 0)  # Calcula o total de páginas

    return {
        "data": membros,  # Lista de membros
        "pagination": {
            "total": total,  # Total de membros
            "current_page": current_page,  # Página atual
            "total_pages": total_pages,  # Total de páginas
            "page_size": limit,  # Tamanho da página
        },
    }

# Endpoint para listar membros com paginação dinâmica (cursor-based)
@app.get("/membros/cursor/", response_model=Dict[str, Any])
def read_membros_cursor(
    last_id: Optional[int] = Query(None),  # ID do último membro exibido na página anterior
    page_size: int = Query(10, ge=1),  # Tamanho da página
    session: Session = Depends(get_session)
):
    if last_id:
        query = select(Membro).where(Membro.id > last_id).limit(page_size)  # Consulta baseando-se no last_id
    else:
        query = select(Membro).limit(page_size)  # Consulta os primeiros membros se last_id não for fornecido
    membros = session.exec(query).all()  # Executa a consulta e retorna os resultados

    return {
        "data": membros,  # Lista de membros
        "pagination": {
            "last_id": membros[-1].id if membros else None,  # Último ID retornado
            "page_size": page_size,  # Tamanho da página
        },
    }

# Endpoint para listar membros filtrados por nome ou email, com paginação
@app.get("/membros/filtrados/", response_model=Dict[str, Any])
def read_filtered_membros(
    nome: Optional[str] = None,  # Filtro opcional por nome
    email: Optional[str] = None,  # Filtro opcional por email
    offset: int = Query(0, ge=0),  # Define o ponto inicial da consulta
    limit: int = Query(10, ge=1),  # Limita o número de resultados por página
    session: Session = Depends(get_session)
):
    query = select(Membro)  # Consulta base inicial
    
    if nome:
        query = query.where(func.lower(Membro.nome).like(f"%{nome.lower()}%"))  # Filtra por nome (case insensitive)
    if email:
        query = query.where(func.lower(Membro.email).like(f"%{email.lower()}%"))  # Filtra por email (case insensitive)
    
    total = session.exec(select(func.count()).select_from(query.subquery())).one_or_none() or (0) # Conta os resultados filtrados
    membros = session.exec(query.offset(offset).limit(limit)).all()  # Aplica offset e limit à consulta
    current_page = (offset // limit) + 1  # Calcula a página atual
    total_pages = (total // limit) + (1 if total % limit > 0 else 0)  # Calcula o total de páginas

    return {
        "data": membros,  
        "pagination": {
            "total": total,  
            "current_page": current_page,  
            "total_pages": total_pages,  
            "page_size": limit, 
        },
    }
