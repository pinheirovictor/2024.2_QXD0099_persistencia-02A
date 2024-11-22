import csv

# Dados de exemplo
dados = [
    {"nome": "Alice", "idade": 25, "curso": "Python"},
    {"nome": "Bob", "idade": 30, "curso": "Data Science"},
    {"nome": "Charlie", "idade": 22, "curso": "Machine Learning"}
]

# Serializar os dados para CSV
with open("dados.csv", "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["nome", "idade", "curso"])
    writer.writeheader()  # Escreve os nomes das colunas
    writer.writerows(dados)  # Escreve cada linha de dados
