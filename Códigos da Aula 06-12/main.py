import psycopg2

# Conectar ao banco de dados
try:
    conn = psycopg2.connect(
        dbname='db1',
        user='postgres',
        password='2023',
        host='localhost',
        port='5432'
    )
    cursor = conn.cursor()

    try:
        # Criar tabela
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alunos (
                id SERIAL PRIMARY KEY,
                nome TEXT NOT NULL
            )
        ''')

        # Inserir dados
        cursor.execute('INSERT INTO alunos (nome) VALUES (%s)', ('Maria',))
        cursor.execute('INSERT INTO alunos (nome) VALUES (%s)', ('João',))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f'Erro ao executar operações no banco de dados: {e}')

    # Consultar dados
    cursor.execute('SELECT * FROM alunos')
    resultados = cursor.fetchall()

    for linha in resultados:
        print(linha)

except Exception as e:
    print(f'Erro ao conectar ao banco de dados: {e}')
finally:
    # Fechar conexões
    if cursor:
        cursor.close()
    if conn:
        conn.close()
