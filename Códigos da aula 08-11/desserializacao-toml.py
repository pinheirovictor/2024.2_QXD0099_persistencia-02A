import toml

# Ler dados do arquivo TOML
with open("dados.toml", "r") as file:
    dados = toml.load(file)

print(dados)
