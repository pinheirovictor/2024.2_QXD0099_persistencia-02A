from fastapi import FastAPI, Depends, HTTPException 
from sqlalchemy.orm import Session 
from models import Aluno, Curso, Inscricao  
from database import get_db  

app = FastAPI()

@app.post("/alunos")
def criar_aluno(nome: str, email: str, db: Session = Depends(get_db)):
    aluno = Aluno(nome=nome, email=email)
    db.add(aluno)
    db.commit()
    db.refresh(aluno)
    return aluno

@app.get("/alunos")
def listar_alunos(db: Session = Depends(get_db)):
    return db.query(Aluno).all

@app.post("/cursos")
def criar_curso(nome: str, descricao: str, db: Session = Depends(get_db)):
    curso = Curso(nome=nome, descricao=descricao)
    db.add(curso)
    db.commit()
    db.refresh(curso)
    return curso

@app.get("/cursos/")
def listar_cursos(db: Session = Depends(get_db)):
    return db.query(Curso).all()


@app.post("/inscricoes")
def criar_inscricao(aluno_id: int, curso_id: int, db: Session = Depends(get_db)):
   
   aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
   curso = db.query(Curso).filter(curso.id == curso_id).first() 
   
   if not aluno or not curso:
        raise HTTPException(status_code=404, detail="Aluno ou Curso não encontrados")
    
   inscricao = Inscricao(aluno_id = aluno_id, curso_id = curso_id)
   db.add(inscricao)
   db.commit()
   db.refresh(inscricao)
   return inscricao


@app.get("/inscricoes")
def listar_inscricoes(db: Session = Depends(get_db)):
    return db.query(Inscricao).all()
    
