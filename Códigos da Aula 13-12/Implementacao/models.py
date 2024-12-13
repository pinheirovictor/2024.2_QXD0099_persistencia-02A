from sqlalchemy.orm import relationship, declarative_base 
from sqlalchemy import Column, Integer, String, ForeignKey

Base = declarative_base()

class Aluno(Base):
    __tablename__ = 'alunos'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    
    inscricoes = relationship('Inscricao', back_populates='aluno')
    

class Curso(Base):
    __tablename__ = 'cursos'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    descricao = Column(String)
    
    inscricoes = relationship('Inscricao', back_populates='curso')
        
        
class Inscricao(Base):
    __tablename__ = 'inscricoes'
    
    id = Column(Integer, primary_key=True)
    aluno_id = Column(Integer, ForeignKey('alunos.id'))
    curso_id = Column(Integer, ForeignKey('cursos.id'))
    
    aluno = relationship('Aluno', back_populates='inscricoes')
    curso = relationship('Curso', back_populates='inscricoes')
    
        
        
        
        