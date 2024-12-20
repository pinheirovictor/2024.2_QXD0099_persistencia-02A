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

# Projeto: Inserir
@app.post("/projetos", response_model=Projeto)
def criar_projeto(projeto: Projeto, session: Session = Depends(get_session)):
    session.add(projeto)
    session.commit()
    session.refresh(projeto)
    return projeto

# Equipe: Inserir
@app.post("/equipes/", response_model=Equipe)
def criar_equipe(equipe: Equipe, session: Session = Depends(get_session)):
    try:
        session.add(equipe)
        session.commit()
        session.refresh(equipe)  # Recarrega o estado do objeto
        return equipe
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao criar equipe: {e}")

# Membro: Inserir
@app.post("/membros/", response_model=Membro)
def criar_membro(membro: Membro, session: Session = Depends(get_session)):
    try:
        session.add(membro)
        session.commit()
        session.refresh(membro)
        return membro
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao criar membro: {e}")

# Tarefa: Inserir
@app.post("/tarefas", response_model=Tarefa)
def criar_tarefa(tarefa: Tarefa, session: Session = Depends(get_session)):
    session.add(tarefa)
    session.commit()
    session.refresh(tarefa)
    return tarefa

# Membro se associa a um projeto (Relacionamento n:m)
@app.post("/membros/{membro_id}/associar/{equipe_id}")
def associar_membro_a_equipe(membro_id: int, equipe_id: int, session: Session = Depends(get_session)):
    # Verifica se o membro existe
    membro = session.get(Membro, membro_id)
    if not membro:
        raise HTTPException(status_code=404, detail="Membro não encontrado.")
    
    # Verifica se a equipe existe
    equipe = session.get(Equipe, equipe_id)
    if not equipe:
        raise HTTPException(status_code=404, detail="Equipe não encontrada.")
    
    try:
        associacao = Membership(membro_id=membro_id, equipe_id=equipe_id)
        session.add(associacao)
        session.commit()
        return {"message": f"Membro {membro.nome} associado à equipe {equipe.nome}"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao criar associação: {e}")



# Listar membros de um projeto
@app.get("/projetos/{projeto_id}/membros", response_model=list[Membro])
def listar_membros_por_projeto(projeto_id: int, session: Session = Depends(get_session)):
    # Valida se o projeto existe
    projeto = session.get(Projeto, projeto_id)
    if not projeto:
        raise HTTPException(status_code=404, detail=f"Projeto com ID {projeto_id} não encontrado.")
    
    # Consulta membros associados ao projeto
    membros = session.exec(
        select(Membro).where(Membro.equipe_id == projeto.equipe_id)
    ).all()

    if not membros:
        raise HTTPException(status_code=404, detail=f"Nenhum membro associado ao projeto com ID {projeto_id}.")
    
    return membros

# Listar projetos de um membro
@app.get("/membros/{membro_id}/projetos", response_model=list[Projeto])
def listar_projetos_por_membro(membro_id: int, session: Session = Depends(get_session)):
    # Valida se o membro existe
    membro = session.get(Membro, membro_id)
    if not membro:
        raise HTTPException(status_code=404, detail=f"Membro com ID {membro_id} não encontrado.")
    
    # Consulta projetos associados ao membro
    projetos = session.exec(
        select(Projeto).join(Equipe).where(Equipe.id == membro.equipe_id)
    ).all()

    if not projetos:
        raise HTTPException(status_code=404, detail=f"Nenhum projeto associado ao membro com ID {membro_id}.")
    
    return projetos


# Listar todas as equipes
@app.get("/equipes", response_model=list[Equipe])
def listar_equipes(session: Session = Depends(get_session)):
    equipes = session.exec(select(Equipe)).all()
    if not equipes:
        raise HTTPException(status_code=404, detail="Nenhuma equipe encontrada.")
    return equipes


# Listar todos os membros de uma equipe
@app.get("/equipes/{equipe_id}/membros", response_model=list[Membro])
def listar_membros_por_equipe(equipe_id: int, session: Session = Depends(get_session)):
    # Valida se a equipe existe
    equipe = session.get(Equipe, equipe_id)
    if not equipe:
        raise HTTPException(status_code=404, detail=f"Equipe com ID {equipe_id} não encontrada.")
    
    # Consulta membros associados à equipe
    membros = session.exec(
        select(Membro).where(Membro.equipe_id == equipe_id)
    ).all()

    if not membros:
        raise HTTPException(status_code=404, detail=f"Nenhum membro encontrado para a equipe com ID {equipe_id}.")
    
    return membros


# Listar todas as tarefas de um projeto
@app.get("/projetos/{projeto_id}/tarefas", response_model=list[Tarefa])
def listar_tarefas_por_projeto(projeto_id: int, session: Session = Depends(get_session)):
    # Valida se o projeto existe
    projeto = session.get(Projeto, projeto_id)
    if not projeto:
        raise HTTPException(status_code=404, detail=f"Projeto com ID {projeto_id} não encontrado.")
    
    # Consulta tarefas associadas ao projeto
    tarefas = session.exec(
        select(Tarefa).where(Tarefa.projeto_id == projeto_id)
    ).all()

    if not tarefas:
        raise HTTPException(status_code=404, detail=f"Nenhuma tarefa encontrada para o projeto com ID {projeto_id}.")
    
    return tarefas