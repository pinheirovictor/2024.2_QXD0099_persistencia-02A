import toml

# Dados de exemplo
dados = {
    "pessoa": {
        "nome": "Alice",
        "idade": 25,
        "cursos": ["Python", "Data Science"]
    },
    "configuracoes": {
        "tema": "escuro",
        "notificacoes": True
    }
}

# Serializar os dados para um arquivo TOML
with open("dados.toml", "w") as file:
    toml.dump(dados, file)
