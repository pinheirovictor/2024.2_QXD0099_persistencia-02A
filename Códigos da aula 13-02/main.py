from fastapi import FastAPI
from database import init_db
from routes.bens_e_direitos import router as bens_e_direitos, delete_bens_e_direitos, update_bens_e_direitos
from routes.faixa_base_calculo_anual import router as faixa_base_calculo_anual
from routes.rendimentos_isentos import router as rendimentos_isentos
from routes.capital_estado import router as capital_estado_residencia
from routes.dividas_e_onus import router as dividas_e_onus
from routes.bens_e_dividas import router as bens_dividas
from routes.complexas import router as consultar_rendimentos_por_estado

app = FastAPI()

# Garantir que o banco de dados seja criado antes de rodar a API
@app.on_event("startup")
async def startup():
    await init_db()

# Registrando as Rotas
app.include_router(bens_e_direitos, prefix="/api")


app.include_router(faixa_base_calculo_anual, prefix="/api")
app.include_router(rendimentos_isentos, prefix="/api")
app.include_router(capital_estado_residencia, prefix="/api")
app.include_router(dividas_e_onus, prefix="/api")
app.include_router(bens_dividas, prefix="/api")

app.include_router(consultar_rendimentos_por_estado, prefix="/api")


@app.get("/")
def root():
    return {"message": "API de Upload de Dados do Imposto de Renda"}
