from sqlmodel import Session
from sqlmodel import SQLModel, Field, create_engine
from modelos import Student

database_url = "mysql+mysqlconnector://student:password@localhost/school_db"
engine = create_engine(database_url, echo=True)

with Session(engine) as session:
    student = Student(name="Alice", age=20, grade="A")
    session.add(student)
    session.commit()
    session.refresh(student)
    print(student)


