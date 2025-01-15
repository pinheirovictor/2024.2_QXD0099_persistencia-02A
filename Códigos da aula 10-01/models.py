# Importa as classes necessárias para definir as colunas da tabela
from sqlalchemy import Column, Integer, String

# Importa a classe Base, que serve como base para a criação de modelos ORM
from database import Base

# Define a classe User, que representa a tabela 'users' no banco de dados
class User(Base):
    # Define o nome da tabela no banco de dados
    __tablename__ = 'users'
    
    # Define a coluna 'id' como a chave primária
    # Integer: tipo de dado inteiro
    # primary_key=True: indica que essa coluna é a chave primária da tabela
    # index=True: cria um índice para essa coluna, melhorando a performance de consultas
    id = Column(Integer, primary_key=True, index=True)
    
    # Define a coluna 'name'
    # String: tipo de dado para armazenar texto
    # index=True: permite buscar usuários pelo nome de forma mais eficiente
    name = Column(String, index=True)
    
    # Define a coluna 'email'
    # unique=True: garante que cada email seja único na tabela (não podem existir emails duplicados)
    # index=True: otimiza buscas baseadas no email
    email = Column(String, unique=True, index=True)