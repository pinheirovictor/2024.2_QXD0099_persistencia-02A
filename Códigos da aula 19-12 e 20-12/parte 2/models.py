from sqlmodel import SQLModel, Field

class Aluno(SQLModel, table=True):
    __tablename__ = 'alunos'
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    apelido: str | None = Field(default=None)


