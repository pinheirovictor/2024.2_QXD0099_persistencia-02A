from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy import func
from sqlmodel import SQLModel, Session, create_engine, select
from models import Membro
from typing import List, Optional, Dict, Any

app = FastAPI()

DATABASE_URL = "sqlite:///database.db"
engine = create_engine(DATABASE_URL, echo=True)


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)
    
    
def get_session():
    with Session(engine) as session:
        yield session
        
        
@app.post("/membros", response_model=Membro)
def create_membro(membro: Membro, session: Session = Depends(get_session)):
    session.add(membro)
    session.commit()
    session.refresh(membro)
    return membro


@app.get("/membros", response_model=list[Membro])
def ler_membros(
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


@app.get("/membros/paginados", response_model=Dict[str, Any])
def ler_membros_paginados(
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    session: Session = Depends(get_session)
):
    total = session.exec(select(func.count(Membro.id))).one_or_none() or 0
    #one_or_none() retorna uma tupla contendo o resultado da contagem.  total[0] extrai o valor numérico da contagem.
    membros = session.exec(select(Membro).offset(offset).limit(limit)).all()
    current_page = (offset // limit) + 1
    total_pages = (total // limit ) + 1  # Cálculo correto do total de páginas
    
    return {
        "data": membros,
        "pagination": {
            "total": total,
            "current_page": current_page,
            "total_pages": total_pages,
            "page_size": limit
        }
    }


@app.get("/membros/cursor", response_model=Dict[str, Any])
def ler_membros_cursor(
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
        "data":membros,
        "pagination":{
            "last_id": membros[-1].id if membros else None,
            "page_size": page_size,
        }
    }
    
    

@app.get("/membros/filtrados", response_model=Dict[str, Any])
def ler_membros_filtrados(
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
        
    total = session.exec(select(func.count()).select_from(query.subquery())).one_or_none() or (0)
    membros = session.exec(query.offset(offset).limit(limit)).all()
    current_page = (offset // limit) + 1
    total_pages = (total // limit) + 1
    
    return {
        "data": membros,  
        "pagination": {
            "total": total,  
            "current_page": current_page,  
            "total_pages": total_pages,  
            "page_size": limit, 
        },
    }

