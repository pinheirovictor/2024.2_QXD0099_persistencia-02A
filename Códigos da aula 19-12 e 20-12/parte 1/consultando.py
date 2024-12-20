from sqlmodel import Session
from sqlmodel import SQLModel, Field, create_engine
from modelos import Student

database_url = "mysql+mysqlconnector://student:password@localhost/school_db"
engine = create_engine(database_url, echo=True)


with Session(engine) as session:
    students = session.query(Student).all()
    for student in students:
        print(student)
