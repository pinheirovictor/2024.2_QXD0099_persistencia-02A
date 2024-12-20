from sqlmodel import SQLModel, Field, create_engine

class Student(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    age: int
    grade: str

database_url = "mysql+mysqlconnector://student:password@localhost/school_db"
engine = create_engine(database_url, echo=True)

# Criar tabelas no banco
SQLModel.metadata.create_all(engine)





