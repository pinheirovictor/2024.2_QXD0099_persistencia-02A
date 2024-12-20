from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from database import create_db_and_tables, get_session
from models import Projeto, Equipe, Membro, Tarefa, Membership

app = FastAPI()

# Inicializa o banco de dados ao iniciar a aplicação
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def home():
    return {"message": "Bem-vindo ao sistema de gerenciamento de projetos"}

# ---------------------------
# CRUD para Projetos
# ---------------------------

# Criar Projeto
@app.post("/projetos", response_model=Projeto)
def criar_projeto(projeto: Projeto, session: Session = Depends(get_session)):
    session.add(projeto)
    session.commit()
    session.refresh(projeto)
    return projeto

# Listar Projetos
@app.get("/projetos", response_model=list[Projeto])
def listar_projetos(session: Session = Depends(get_session)):
    return session.exec(select(Projeto)).all()

# Buscar Projeto por ID
@app.get("/projetos/{projeto_id}", response_model=Projeto)
def buscar_projeto(projeto_id: int, session: Session = Depends(get_session)):
    projeto = session.get(Projeto, projeto_id)
    if not projeto:
        raise HTTPException(status_code=404, detail="Projeto não encontrado.")
    return projeto

# Atualizar Projeto
@app.put("/projetos/{projeto_id}", response_model=Projeto)
def atualizar_projeto(projeto_id: int, projeto: Projeto, session: Session = Depends(get_session)):
    projeto_existente = session.get(Projeto, projeto_id)
    if not projeto_existente:
        raise HTTPException(status_code=404, detail="Projeto não encontrado.")
    
    for key, value in projeto.dict(exclude_unset=True).items():
        setattr(projeto_existente, key, value)

    session.add(projeto_existente)
    session.commit()
    session.refresh(projeto_existente)
    return projeto_existente

# Excluir Projeto
@app.delete("/projetos/{projeto_id}", response_model=dict)
def excluir_projeto(projeto_id: int, session: Session = Depends(get_session)):
    projeto = session.get(Projeto, projeto_id)
    if not projeto:
        raise HTTPException(status_code=404, detail="Projeto não encontrado.")
    session.delete(projeto)
    session.commit()
    return {"message": "Projeto excluído com sucesso."}

# ---------------------------
# CRUD para Equipes
# ---------------------------

@app.post("/equipes", response_model=Equipe)
def criar_equipe(equipe: Equipe, session: Session = Depends(get_session)):
    session.add(equipe)
    session.commit()
    session.refresh(equipe)
    return equipe

@app.get("/equipes", response_model=list[Equipe])
def listar_equipes(session: Session = Depends(get_session)):
    return session.exec(select(Equipe)).all()

@app.get("/equipes/{equipe_id}", response_model=Equipe)
def buscar_equipe(equipe_id: int, session: Session = Depends(get_session)):
    equipe = session.get(Equipe, equipe_id)
    if not equipe:
        raise HTTPException(status_code=404, detail="Equipe não encontrada.")
    return equipe

@app.put("/equipes/{equipe_id}", response_model=Equipe)
def atualizar_equipe(equipe_id: int, equipe: Equipe, session: Session = Depends(get_session)):
    equipe_existente = session.get(Equipe, equipe_id)
    if not equipe_existente:
        raise HTTPException(status_code=404, detail="Equipe não encontrada.")
    
    for key, value in equipe.dict(exclude_unset=True).items():
        setattr(equipe_existente, key, value)

    session.add(equipe_existente)
    session.commit()
    session.refresh(equipe_existente)
    return equipe_existente

@app.delete("/equipes/{equipe_id}", response_model=dict)
def excluir_equipe(equipe_id: int, session: Session = Depends(get_session)):
    equipe = session.get(Equipe, equipe_id)
    if not equipe:
        raise HTTPException(status_code=404, detail="Equipe não encontrada.")
    session.delete(equipe)
    session.commit()
    return {"message": "Equipe excluída com sucesso."}

# ---------------------------
# CRUD para Membros
# ---------------------------

@app.post("/membros", response_model=Membro)
def criar_membro(membro: Membro, session: Session = Depends(get_session)):
    session.add(membro)
    session.commit()
    session.refresh(membro)
    return membro

@app.get("/membros", response_model=list[Membro])
def listar_membros(session: Session = Depends(get_session)):
    return session.exec(select(Membro)).all()

@app.get("/membros/{membro_id}", response_model=Membro)
def buscar_membro(membro_id: int, session: Session = Depends(get_session)):
    membro = session.get(Membro, membro_id)
    if not membro:
        raise HTTPException(status_code=404, detail="Membro não encontrado.")
    return membro

@app.put("/membros/{membro_id}", response_model=Membro)
def atualizar_membro(membro_id: int, membro: Membro, session: Session = Depends(get_session)):
    membro_existente = session.get(Membro, membro_id)
    if not membro_existente:
        raise HTTPException(status_code=404, detail="Membro não encontrado.")
    
    for key, value in membro.dict(exclude_unset=True).items():
        setattr(membro_existente, key, value)

    session.add(membro_existente)
    session.commit()
    session.refresh(membro_existente)
    return membro_existente

@app.delete("/membros/{membro_id}", response_model=dict)
def excluir_membro(membro_id: int, session: Session = Depends(get_session)):
    membro = session.get(Membro, membro_id)
    if not membro:
        raise HTTPException(status_code=404, detail="Membro não encontrado.")
    session.delete(membro)
    session.commit()
    return {"message": "Membro excluído com sucesso."}

# ---------------------------
# CRUD para Tarefas
# ---------------------------

@app.post("/tarefas", response_model=Tarefa)
def criar_tarefa(tarefa: Tarefa, session: Session = Depends(get_session)):
    session.add(tarefa)
    session.commit()
    session.refresh(tarefa)
    return tarefa

@app.get("/tarefas", response_model=list[Tarefa])
def listar_tarefas(session: Session = Depends(get_session)):
    return session.exec(select(Tarefa)).all()

@app.get("/tarefas/{tarefa_id}", response_model=Tarefa)
def buscar_tarefa(tarefa_id: int, session: Session = Depends(get_session)):
    tarefa = session.get(Tarefa, tarefa_id)
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada.")
    return tarefa

@app.put("/tarefas/{tarefa_id}", response_model=Tarefa)
def atualizar_tarefa(tarefa_id: int, tarefa: Tarefa, session: Session = Depends(get_session)):
    tarefa_existente = session.get(Tarefa, tarefa_id)
    if not tarefa_existente:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada.")
    
    for key, value in tarefa.dict(exclude_unset=True).items():
        setattr(tarefa_existente, key, value)

    session.add(tarefa_existente)
    session.commit()
    session.refresh(tarefa_existente)
    return tarefa_existente

@app.delete("/tarefas/{tarefa_id}", response_model=dict)
def excluir_tarefa(tarefa_id: int, session: Session = Depends(get_session)):
    tarefa = session.get(Tarefa, tarefa_id)
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada.")
    session.delete(tarefa)
    session.commit()
    return {"message": "Tarefa excluída com sucesso."}
