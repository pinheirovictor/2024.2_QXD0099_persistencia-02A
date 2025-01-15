from sqlmodel import SQLModel, Field
from typing import Optional

class Membro(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    email: str
    
    