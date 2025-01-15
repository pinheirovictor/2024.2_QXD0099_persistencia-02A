# Importa a classe FastAPI, que é usada para criar a aplicação web
from fastapi import FastAPI

# Importa a classe Base dos modelos para acessar as definições de tabelas
from models import Base

# Importa o engine do banco de dados, necessário para vincular as tabelas ao banco
from database import engine

# Importa o roteador configurado no arquivo crud, que contém as rotas CRUD
from crud import router

# Importa o módulo de logging para registrar informações e mensagens da aplicação
import logging

# Importa a classe Request para manipular informações das requisições HTTP
from fastapi import Request

# Importa a função time, usada para medir o tempo de execução de uma requisição
import time

# Inicializa a aplicação FastAPI
app = FastAPI()

# Cria as tabelas no banco de dados a partir dos modelos definidos
Base.metadata.create_all(bind=engine)

# Adiciona o roteador configurado no arquivo crud à aplicação
app.include_router(router)

# Configuração básica do sistema de logs
# Define o nível de log como INFO, o que significa que mensagens informativas e mais importantes serão registradas
logging.basicConfig(level=logging.INFO)

# Middleware para registrar logs de requisições HTTP
@app.middleware("http")
async def log_requests(request: Request, call_next):
    # Cria um logger com o nome "app"
    logger = logging.getLogger("app")
    
    # Registra informações sobre a requisição recebida (método e URL)
    logger.info(f"Recebendo requisição: {request.method} {request.url}")
    
    # Passa a requisição para o próximo middleware ou rota
    response = await call_next(request)
    
    # Registra o status da resposta enviada
    logger.info(f"Resposta: {response.status_code}")
    
    # Retorna a resposta ao cliente
    return response

# Middleware para medir o tempo de execução de cada requisição
@app.middleware("http")
async def measure_execution_time(request: Request, call_next):
    # Marca o tempo inicial antes de processar a requisição
    start_time = time.time()
    
    # Passa a requisição para o próximo middleware ou rota
    response = await call_next(request)
    
    # Calcula o tempo total de processamento
    process_time = time.time() - start_time
    
    # Registra o tempo de execução nos logs
    logging.info(f"Tempo de execução: {process_time:.4f} segundos")
    
    # Retorna a resposta ao cliente
    return response


# Explicação dos principais componentes:
# Base.metadata.create_all(bind=engine):

# Cria automaticamente as tabelas no banco de dados com base nos modelos definidos em models.py.
# O engine especifica a conexão com o banco.
# app.include_router(router):

# Adiciona as rotas definidas no roteador (arquivo crud.py) à aplicação FastAPI.
# Facilita a modularização e reutilização de código.
# Middlewares:

# São funções que processam as requisições antes ou depois que elas alcançam as rotas específicas.
# a. log_requests:

# Registra informações sobre cada requisição recebida e a respectiva resposta.
# Útil para depuração e auditoria.
# b. measure_execution_time:

# Mede o tempo total que a aplicação leva para processar cada requisição.
# Importante para monitorar o desempenho da aplicação.
# Logs:

# Os logs ajudam a acompanhar o funcionamento da aplicação e a identificar problemas.
# Aqui, configuramos o nível INFO para registrar informações úteis sobre requisições e respostas.



from fastapi import FastAPI
from models import Base
from database import engine
from crud import router
import logging
from fastapi import Request
import time

app = FastAPI()

# Criar tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Adicionar o roteador
app.include_router(router)


#Logs
logging.basicConfig(level=logging.INFO)

# @app.middleware("http")
# async def log_requests(request: Request, call_next):
#     logger = logging.getLogger("app")
#     logger.info(f"Recebendo requisição: {request.method} {request.url}")
#     response = await call_next(request)
#     logger.info(f"Resposta: {response.status_code}")
#     return response

# @app.middleware("http")
# async def measure_execution_time(request: Request, call_next):
#     start_time = time.time()
#     response = await call_next(request)
#     process_time = time.time() - start_time
#     logging.info(f"Tempo de execução: {process_time:.4f} segundos")
#     return response

