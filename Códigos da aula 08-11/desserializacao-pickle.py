import pickle

# Ler o arquivo e desserializar o objeto
with open("dados.pkl", "rb") as file:
    dados_carregados = pickle.load(file)

print("Dados desserializados:", dados_carregados)
