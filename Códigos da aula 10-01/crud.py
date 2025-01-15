# Importa o SQLAlchemyCRUDRouter da biblioteca fastapi_crudrouter, 
# que fornece um roteador pronto para operações CRUD (Create, Read, Update, Delete)
from fastapi_crudrouter import SQLAlchemyCRUDRouter

# Importa o modelo User definido na aplicação
from models import User

# Importa a função get_db, que é usada para gerenciar as sessões de banco de dados
from database import get_db

# Importa a classe BaseModel da biblioteca Pydantic, que será usada para criar esquemas de validação
from pydantic import BaseModel

# Definição do esquema Pydantic para validação de dados do modelo User
class UserSchema(BaseModel):
    id: int  # Campo obrigatório representando o ID do usuário
    name: str  # Campo obrigatório representando o nome do usuário
    email: str  # Campo obrigatório representando o email do usuário

    # Configuração adicional para o esquema Pydantic
    class Config:
        orm_mode = True  # Habilita o suporte para interagir diretamente com objetos ORM

# Configuração do roteador CRUD utilizando o SQLAlchemyCRUDRouter
router = SQLAlchemyCRUDRouter(
    schema=UserSchema,  # Especifica o esquema Pydantic para validação de dados
    db_model=User,      # Indica o modelo SQLAlchemy correspondente ao esquema
    db=get_db           # Define a função que retorna a sessão do banco de dados
)


# Explicação dos principais componentes:
# UserSchema:

# É uma classe derivada de BaseModel (do Pydantic) que serve como uma representação dos dados que serão enviados ou recebidos via API.
# O orm_mode habilitado na configuração permite que objetos retornados pelo ORM (SQLAlchemy) sejam automaticamente convertidos para este esquema.
# SQLAlchemyCRUDRouter:

# Esta classe cria automaticamente todas as rotas básicas (como GET, POST, PUT, DELETE) para interagir com o banco de dados.
# As rotas são baseadas no modelo SQLAlchemy (User) e no esquema Pydantic (UserSchema).
# O parâmetro db define como as sessões do banco de dados serão gerenciadas, garantindo que cada requisição tenha sua própria sessão.
# get_db:

# É uma função que fornece uma sessão de banco de dados para cada requisição, geralmente implementada com o uso de yield para garantir que a sessão seja corretamente aberta e fechada.

# from fastapi_crudrouter import SQLAlchemyCRUDRouter
# from models import User
# from database import get_db
# from pydantic import BaseModel

# # Criar esquema Pydantic
# class UserSchema(BaseModel):
#     id: int
#     name: str
#     email: str

#     class Config:
#         orm_mode = True  # Permite trabalhar com objetos ORM diretamente

# # Configurar o roteador CRUD
# router = SQLAlchemyCRUDRouter(
#     schema=UserSchema,  # Esquema Pydantic
#     db_model=User,      # Modelo SQLAlchemy
#     db=get_db
# )
