# Importação do framework FastAPI para construção de APIs
from fastapi import FastAPI

# Importação das rotas organizadas em módulos separados
from routes import (
    curso_routes, professor_routes, aluno_routes, 
    turma_routes, departamento_routes, acao
)

# Criação da instância principal da aplicação FastAPI
app = FastAPI()

# Inclusão das rotas específicas para cada entidade do sistema acadêmico
app.include_router(curso_routes.router, prefix="/cursos", tags=["Cursos"])
app.include_router(professor_routes.router, prefix="/professores", tags=["Professores"])
app.include_router(aluno_routes.router, prefix="/alunos", tags=["Alunos"])
app.include_router(turma_routes.router, prefix="/turmas", tags=["Turmas"])
app.include_router(departamento_routes.router, prefix="/departamentos", tags=["Departamentos"])
app.include_router(acao.router, prefix="/acao", tags=["Ação"])

# Rota raiz da API, apenas para verificar se a aplicação está rodando
@app.get("/")
def home():
    return {"message": "API de Gestão Acadêmica com FastAPI e MongoDB"}


