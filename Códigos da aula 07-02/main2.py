from fastapi import FastAPI, UploadFile, File, HTTPException
from pymongo import MongoClient
import gridfs
from bson import ObjectId
from fastapi.responses import StreamingResponse

app = FastAPI()

# Conectar ao MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["meuBanco"]
fs = gridfs.GridFS(db, collection="uploads")

# Upload de arquivo para GridFS
@app.post("/upload/")
async def upload_arquivo(file: UploadFile = File(...)):
    file_id = fs.put(file.file, filename=file.filename)
    return {"mensagem": "Arquivo enviado com sucesso", "file_id": str(file_id)}


@app.get("/download/{file_id}")
async def download_arquivo(file_id: str):
    try:
        object_id = ObjectId(file_id)  # Converter file_id para ObjectId
        file = fs.get(object_id)

        return StreamingResponse(file, media_type="application/octet-stream", headers={
            "Content-Disposition": f"attachment; filename={file.filename}"
        })
    except gridfs.NoFile:
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/arquivos/")
async def listar_arquivos():
    arquivos = db["uploads.files"].find({}, {"_id": 1, "filename": 1})  # Buscar arquivos com ID e nome

    return [{"file_id": str(doc["_id"]), "filename": doc["filename"]} for doc in arquivos]

@app.delete("/delete/{file_id}")
async def deletar_arquivo(file_id: str):
    try:
        object_id = ObjectId(file_id)  # Converter string para ObjectId
        fs.delete(object_id)  # Deletar arquivo do GridFS
        return {"mensagem": "Arquivo deletado com sucesso"}
    except gridfs.NoFile:
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
