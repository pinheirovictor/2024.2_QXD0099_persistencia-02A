import json

# Ler o arquivo e desserializar os dados JSON
with open("dados.json", "r") as file:
    dados_carregados = json.load(file)

print("Dados desserializados do JSON:", dados_carregados)
