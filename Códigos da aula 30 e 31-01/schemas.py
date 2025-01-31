# Importação da classe base do Pydantic para validação de dados
from pydantic import BaseModel, Field

# Importação de tipos para anotações de listas e valores opcionais
from typing import List, Optional

# Definição do modelo de dados para um Professor
class Professor(BaseModel):
    id: Optional[str] = Field(None, alias="_id")  # Campo opcional representando o ID no MongoDB
    nome: str  # Nome do professor
    especialidade: str  # Área de especialização do professor
    email: str  # Email do professor

# Definição do modelo de dados para um Curso
class Curso(BaseModel):
    id: Optional[str] = Field(None, alias="_id")  # ID do curso, compatível com MongoDB
    nome: str  # Nome do curso
    descricao: str  # Descrição do curso
    carga_horaria: int  # Carga horária total do curso
    professor_id: str  # ID do professor responsável pelo curso (Relacionamento 1:1)
    alunos: Optional[List[str]] = []  # Lista de IDs dos alunos matriculados (Relacionamento 1:N)

# Definição do modelo de dados para um Aluno
class Aluno(BaseModel):
    id: Optional[str] = Field(None, alias="_id")  # ID do aluno
    nome: str  # Nome do aluno
    email: str  # Email do aluno
    idade: int  # Idade do aluno
    cursos: Optional[List[str]] = []  # Lista de IDs dos cursos em que o aluno está matriculado (Relacionamento N:N)

# Definição do modelo de dados para uma Turma
class Turma(BaseModel):
    id: Optional[str] = Field(None, alias="_id")  # ID da turma
    nome: str  # Nome da turma
    curso_id: str  # ID do curso ao qual a turma pertence (Relacionamento 1:N)
    alunos: List[str]  # Lista de IDs dos alunos matriculados na turma (Relacionamento N:N)

# Definição do modelo de dados para um Departamento
class Departamento(BaseModel):
    id: Optional[str] = Field(None, alias="_id")  # ID do departamento
    nome: str  # Nome do departamento acadêmico
    chefe_id: Optional[str]  # ID do professor chefe do departamento (Relacionamento 1:1)
    cursos: List[str]  # Lista de IDs dos cursos pertencentes ao departamento (Relacionamento 1:N)


