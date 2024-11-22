import json

dados = {"nome": "Alice", "idade": 25, "cursos": ["Python", "Data Science"]}

# Serializar para JSON e salvar em um arquivo
with open("dados.json", "w") as file:
    json.dump(dados, file)
