# Exemplo de leitura de arquivo 

# Abre o arquivo "arquivo.txt" para leitura em modo binário 
with open('arquivo.txt', 'rb') as file: # 'rb' significa leitura em modo binário 
    b = file.read(200) # Lê o primeiro byte do arquivo 

# Exibe o valor do byte lido 
print(b)
