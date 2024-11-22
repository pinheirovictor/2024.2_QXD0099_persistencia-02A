import yaml

dados = {"nome": "Alice", "idade": 25, "cursos": ["Python", "Data Science"]}

# Serializar para YAML e salvar em um arquivo
with open("dados.yaml", "w") as file:
    yaml.dump(dados, file)
