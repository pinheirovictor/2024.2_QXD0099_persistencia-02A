from fastapi import FastAPI, HTTPException
from pymongo import MongoClient, GEOSPHERE
from pydantic import BaseModel
from typing import List


app = FastAPI()

# Conectar ao MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["geodb"]
collection = db["locais"]

# Criar índice geoespacial
collection.create_index([("localizacao", GEOSPHERE)])

# Modelo Pydantic para entrada de dados
class Local(BaseModel):
    nome: str
    latitude: float
    longitude: float

# Rota para cadastrar um local
@app.post("/locais/")
async def cadastrar_local(local: Local):
    doc = {
        "nome": local.nome,
        "localizacao": {
            "type": "Point",
            "coordinates": [local.longitude, local.latitude]
        }
    }
    collection.insert_one(doc)
    return {"mensagem": "Local cadastrado com sucesso"}

# Rota para listar locais
@app.get("/locais/", response_model=List[Local])
async def listar_locais():
    locais = collection.find()
    return [
        {"nome": doc["nome"], "latitude": doc["localizacao"]["coordinates"][1], "longitude": doc["localizacao"]["coordinates"][0]}
        for doc in locais
    ]


# Rota para buscar locais próximos
@app.get("/locais/proximos/")
async def buscar_locais(latitude: float, longitude: float, max_distancia: int = 5000):
    resultado = collection.find({
        "localizacao": {
            "$near": {
                "$geometry": {"type": "Point", "coordinates": [longitude, latitude]},
                "$maxDistance": max_distancia
            }
        }
    })

    locais = [{"nome": doc["nome"], "latitude": doc["localizacao"]["coordinates"][1], "longitude": doc["localizacao"]["coordinates"][0]} for doc in resultado]
    
    if not locais:
        raise HTTPException(status_code=404, detail="Nenhum local encontrado próximo")

    return locais




# Modelo para entrada de dados (coordenadas do polígono)
class PoligonoRequest(BaseModel):
    coordenadas: List[List[float]]  # Lista de pontos [longitude, latitude]

@app.post("/locais/area/")
async def buscar_locais_dentro_area(poligono: PoligonoRequest):
    # Fechar o polígono (último ponto deve ser igual ao primeiro)
    if poligono.coordenadas[0] != poligono.coordenadas[-1]:
        poligono.coordenadas.append(poligono.coordenadas[0])

    # Definir o polígono no formato GeoJSON
    area = {
        "type": "Polygon",
        "coordinates": [poligono.coordenadas]
    }

    # Buscar locais dentro do polígono
    resultado = collection.find({
        "localizacao": {
            "$geoWithin": {
                "$geometry": area
            }
        }
    })

    # Formatar resposta
    locais = [
        {"nome": doc["nome"], "latitude": doc["localizacao"]["coordinates"][1], "longitude": doc["localizacao"]["coordinates"][0]}
        for doc in resultado
    ]

    if not locais:
        raise HTTPException(status_code=404, detail="Nenhum local encontrado dentro da área")

    return locais


# {
#   "coordenadas": [
#     [-46.6400, -23.5600],
#     [-46.6200, -23.5600],
#     [-46.6200, -23.5400],
#     [-46.6400, -23.5400],
#     [-46.6400, -23.5600]
#   ]
# }
