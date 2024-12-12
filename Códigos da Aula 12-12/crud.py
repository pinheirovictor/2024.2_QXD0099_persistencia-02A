import psycopg2
from psycopg2.extras import RealDictCursor

def get_connection():
    return psycopg2.connect(
        database="db1",
        user="postgres",
        password="2023",
        host="localhost",
        port="5432"
    )

# CRUD para Usuário
def create_usuario(nome: str, email: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usuario (nome, email) VALUES (%s, %s) RETURNING id", (nome, email))
    user_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return user_id

def list_usuarios():
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM usuario")
    usuarios = cursor.fetchall()
    cursor.close()
    conn.close()
    return usuarios
