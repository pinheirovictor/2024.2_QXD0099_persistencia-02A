# Exemplo de leitura de um arquivo com codificação específica e conversão para Unicode

# Abre o arquivo "arquivo.txt" para leitura com a codificação UTF-8 (ou outra se necessário)
with open('arquivo.txt', 'r', encoding='utf-8') as file:  # Aqui 'utf-8' pode ser substituído por 'iso-8859-1' se necessário
    c = file.read()  # Lê o primeiro caractere do arquivo

# Exibe o caractere lido
print(c)
