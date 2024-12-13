from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String

# Classe base para o ORM
class Base(DeclarativeBase):
    pass

# Definição de uma tabela como classe
class Aluno(Base):
    __tablename__ = 'alunos'
   
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(50))
    apelido: Mapped[str | None]  # Campo opcional

    # Método para representar os atributos do objeto
    def __repr__(self) -> str:
        return f"Aluno(id={self.id}, nome={self.nome}, apelido={self.apelido})"

