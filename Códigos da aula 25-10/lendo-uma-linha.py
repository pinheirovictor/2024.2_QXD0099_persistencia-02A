# Abrindo o arquivo para leitura de uma linha
with open('arquivo.txt', 'r', encoding='utf-8') as file:
    s = file.readline()  # Lê uma linha do arquivo

# Exibe a linha lida
print(s)
