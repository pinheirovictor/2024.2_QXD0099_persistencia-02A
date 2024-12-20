from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional

class Equipe(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    nome: str
    descricao: Optional[str] = None
    membros: List["Membro"] = Relationship(back_populates="equipe")
    projetos: List["Projeto"] = Relationship(back_populates="equipe")

class Membro(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    nome: str
    equipe_id: int = Field(foreign_key="equipe.id")
    equipe: Optional[Equipe] = Relationship(back_populates="membros")


class Projeto(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    nome: str
    descricao: Optional[str] = None
    equipe_id: int = Field(foreign_key="equipe.id")
    equipe: Optional[Equipe] = Relationship(back_populates="projetos")
    tarefas: List["Tarefa"] = Relationship(back_populates="projeto")  # Adicionado corretamente


class Tarefa(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    descricao: str
    projeto_id: int = Field(foreign_key="projeto.id")
    projeto: Optional[Projeto] = Relationship(back_populates="tarefas")  # Back-populate ajustado


class Membership(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    membro_id: int = Field(foreign_key="membro.id")
    equipe_id: int = Field(foreign_key="equipe.id")
