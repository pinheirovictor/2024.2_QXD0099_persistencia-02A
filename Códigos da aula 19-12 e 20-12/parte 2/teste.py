from dotenv import load_dotenv
import os

# Carregar variáveis do arquivo db.env
load_dotenv("db.env")

# Obter a variável DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("A variável DATABASE_URL não está configurada corretamente.")

print(f"URL do banco de dados: {DATABASE_URL}")
