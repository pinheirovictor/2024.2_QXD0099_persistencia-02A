import json

# Leitura do arquivo JSON
with open("dados.json", "r") as file:
    data = json.load(file)

# # Exemplo de acesso aos dados
# print(data["clientes"])  # substitua por uma chave real no JSON

# Imprime o JSON formatado
print(json.dumps(data, indent=4, ensure_ascii=False))
