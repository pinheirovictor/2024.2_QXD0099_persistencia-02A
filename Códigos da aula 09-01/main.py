from fastapi import FastAPI, HTTPException, Query, Depends
from sqlalchemy import func
from sqlmodel import SQLModel, Session, create_engine, select
from typing import List, Optional, Dict, Any
from models import Membro

app = FastAPI()

# Banco de dados SQLite
DATABASE_URL = "sqlite:///database.db"
engine = create_engine(DATABASE_URL, echo=True)

# Função para criar as tabelas no banco de dados
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

# Função para criar uma sessão do banco de dados
def get_session():
    with Session(engine) as session:
        yield session
        
 
# Criar um membro
@app.post("/membros/", response_model=Membro)
def create_membro(membro: Membro, session: Session = Depends(get_session)):
    session.add(membro)
    session.commit()
    session.refresh(membro)
    return membro

# Ler membros com paginação
@app.get("/membros/", response_model=List[Membro])
def read_membros(
    last_id: Optional[int] = Query(None), 
    page_size: int = Query(10), 
    session: Session = Depends(get_session)
):
    if last_id:
        query = select(Membro).where(Membro.id > last_id).limit(page_size)
    else:
        query = select(Membro).limit(page_size)
    membros = session.exec(query).all()
    return membros

# Ler um membro específico
@app.get("/membros/{membro_id}", response_model=Membro)
def read_membro(membro_id: int, session: Session = Depends(get_session)):
    membro = session.get(Membro, membro_id)
    if not membro:
        raise HTTPException(status_code=404, detail="Membro não encontrado")
    return membro

# Atualizar um membro
@app.put("/membros/{membro_id}", response_model=Membro)
def update_membro(membro_id: int, membro: Membro, session: Session = Depends(get_session)):
    db_membro = session.get(Membro, membro_id)
    if not db_membro:
        raise HTTPException(status_code=404, detail="Membro não encontrado")
    for key, value in membro.dict(exclude_unset=True).items():
        setattr(db_membro, key, value)
    session.add(db_membro)
    session.commit()
    session.refresh(db_membro)
    return db_membro

# Deletar um membro
@app.delete("/membros/{membro_id}")
def delete_membro(membro_id: int, session: Session = Depends(get_session)):
    membro = session.get(Membro, membro_id)
    if not membro:
        raise HTTPException(status_code=404, detail="Membro não encontrado")
    session.delete(membro)
    session.commit()
    return {"detail": "Membro deletado com sucesso"}

# Paginação com informações adicionais (offset/limit)
@app.get("/membros/paginados/", response_model=Dict[str, Any])
def read_membros_paginated(
    offset: int = Query(0, ge=0), 
    limit: int = Query(10, ge=1), 
    session: Session = Depends(get_session)
):
    total = session.exec(select(func.count(Membro.id))).scalar()
    membros = session.exec(select(Membro).offset(offset).limit(limit)).all()
    current_page = (offset // limit) + 1
    total_pages = (total // limit) + (1 if total % limit > 0 else 0)

    return {
        "data": membros,
        "pagination": {
            "total": total,
            "current_page": current_page,
            "total_pages": total_pages,
            "page_size": limit,
        },
    }

# Paginação dinâmica com last_id (cursor-based)
@app.get("/membros/cursor/", response_model=Dict[str, Any])
def read_membros_cursor(
    last_id: Optional[int] = Query(None), 
    page_size: int = Query(10, ge=1), 
    session: Session = Depends(get_session)
):
    if last_id:
        query = select(Membro).where(Membro.id > last_id).limit(page_size)
    else:
        query = select(Membro).limit(page_size)
    membros = session.exec(query).all()

    return {
        "data": membros,
        "pagination": {
            "last_id": membros[-1].id if membros else None,
            "page_size": page_size,
        },
    }

# Consulta paginada com filtros opcionais
@app.get("/membros/filtrados/", response_model=Dict[str, Any])
def read_filtered_membros(
    nome: Optional[str] = None, 
    email: Optional[str] = None, 
    offset: int = Query(0, ge=0), 
    limit: int = Query(10, ge=1), 
    session: Session = Depends(get_session)
):
    query = select(Membro)
    
    if nome:
        query = query.where(func.lower(Membro.nome).like(f"%{nome.lower()}%"))
    if email:
        query = query.where(func.lower(Membro.email).like(f"%{email.lower()}%"))
    
    total = session.exec(select(func.count()).select_from(query.subquery())).scalar()
    membros = session.exec(query.offset(offset).limit(limit)).all()
    current_page = (offset // limit) + 1
    total_pages = (total // limit) + (1 if total % limit > 0 else 0)

    return {
        "data": membros,
        "pagination": {
            "total": total,
            "current_page": current_page,
            "total_pages": total_pages,
            "page_size": limit,
        },
    }
