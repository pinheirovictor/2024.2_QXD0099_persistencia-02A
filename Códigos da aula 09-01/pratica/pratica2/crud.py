from fastapi_crudrouter import SQLAlchemyCRUDRouter
from models import User
from databse import get_db
from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    nome: str
    email: str
    
    class Config:
        orm_mode = True
        
router = SQLAlchemyCRUDRouter(
    schema=UserSchema,
    db_model=User,
    db=get_db
)