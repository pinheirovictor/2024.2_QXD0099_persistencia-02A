from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, SessionLocal

# Conexão com o PostgreSQL
POSTGRES_DATABASE_URL = "postgresql+psycopg2://postgres:2023@localhost/dbmigration"
postgres_engine = create_engine(POSTGRES_DATABASE_URL)

# Copiar dados de SQLite para PostgreSQL
def migrate_data():
    sqlite_session = SessionLocal()
    postgres_session = sessionmaker(bind=postgres_engine)()

    users = sqlite_session.query(User).all()
    for user in users:
        # Crie uma nova instância do objeto User para desvincular da sessão SQLite
        new_user = User(id=user.id, name=user.name, email=user.email)
        postgres_session.add(new_user)
    
    postgres_session.commit()

    sqlite_session.close()
    postgres_session.close()

if __name__ == "__main__":
    migrate_data()
