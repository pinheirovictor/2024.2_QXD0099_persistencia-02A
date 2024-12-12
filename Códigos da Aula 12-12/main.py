from fastapi import FastAPI, HTTPException
from crud import create_usuario, list_usuarios
from db import create_tables, get_connection
from psycopg2.extras import RealDictCursor

app = FastAPI()

# Criação das tabelas no banco
create_tables()

@app.post("/usuarios/")
def criar_usuario(nome: str, email: str):
    user_id = create_usuario(nome, email)
    return {"id": user_id, "nome": nome, "email": email}

@app.get("/usuarios/")
def listar_usuarios():
    return list_usuarios()

@app.get("/pedidos/")
def listar_pedidos():
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """
        SELECT p.id AS pedido_id, u.nome AS usuario, p.data_pedido, p.status
        FROM pedido p
        INNER JOIN usuario u ON p.usuario_id = u.id
    """
    cursor.execute(query)
    pedidos = cursor.fetchall()
    cursor.close()
    conn.close()
    return pedidos

@app.get("/usuarios_com_pedidos/")
def usuarios_com_pedidos():
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """
        SELECT u.nome, p.id AS pedido_id
        FROM usuario u
        LEFT JOIN pedido p ON u.id = p.usuario_id
    """
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

@app.get("/pedidos_sem_usuarios/")
def pedidos_sem_usuarios():
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """
        SELECT p.id AS pedido_id, p.data_pedido, p.status, u.nome AS usuario
        FROM pedido p
        RIGHT JOIN usuario u ON p.usuario_id = u.id
    """
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

@app.get("/todos_usuarios_pedidos/")
def todos_usuarios_pedidos():
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """
        SELECT u.nome AS usuario, p.id AS pedido_id, p.data_pedido, p.status
        FROM usuario u
        FULL OUTER JOIN pedido p ON u.id = p.usuario_id
    """
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results


@app.get("/analise_usuarios/")
def analise_usuarios():
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """
        SELECT 
            u.nome AS usuario,
            COUNT(p.id) AS total_pedidos,
            SUM(pp.quantidade * pr.preco) AS total_gasto,
            AVG(pp.quantidade * pr.preco) AS gasto_medio_por_pedido,
            MAX(pp.quantidade * pr.preco) AS maior_pedido,
            MIN(pp.quantidade * pr.preco) AS menor_pedido
        FROM 
            usuario u
        LEFT JOIN 
            pedido p ON u.id = p.usuario_id
        LEFT JOIN 
            pedido_produto pp ON p.id = pp.pedido_id
        LEFT JOIN 
            produto pr ON pp.produto_id = pr.id
        GROUP BY 
            u.id, u.nome
        ORDER BY 
            total_gasto DESC, total_pedidos DESC;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

@app.put("/usuarios/{usuario_id}/")
def atualizar_usuario(usuario_id: int, nome: str = None, email: str = None):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Verificar se o usuário existe
        cursor.execute("SELECT * FROM usuario WHERE id = %s", (usuario_id,))
        usuario = cursor.fetchone()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        # Atualizar os campos
        if nome:
            cursor.execute("UPDATE usuario SET nome = %s WHERE id = %s", (nome, usuario_id))
        if email:
            cursor.execute("UPDATE usuario SET email = %s WHERE id = %s", (email, usuario_id))

        conn.commit()
        return {"message": "Usuário atualizado com sucesso"}
    finally:
        cursor.close()
        conn.close()
        
        
@app.delete("/usuarios/{usuario_id}/")
def deletar_usuario(usuario_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Verificar se o usuário existe
        cursor.execute("SELECT * FROM usuario WHERE id = %s", (usuario_id,))
        usuario = cursor.fetchone()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        # Deletar o usuário
        cursor.execute("DELETE FROM usuario WHERE id = %s", (usuario_id,))
        conn.commit()
        return {"message": "Usuário deletado com sucesso"}
    finally:
        cursor.close()
        conn.close()