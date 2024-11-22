import yaml

# Ler o arquivo YAML e desserializar
with open("dados.yaml", "r") as file:
    dados_carregados = yaml.safe_load(file)

print("Dados desserializados do YAML:", dados_carregados)
