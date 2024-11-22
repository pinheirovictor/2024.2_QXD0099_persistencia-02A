# Abre o arquivo "saida.txt" para escrita
with open('saida.txt', 'w', encoding='utf-8') as file:
    # Usa a função print para escrever "Java" no arquivo com uma nova linha automaticamente
    print("Java", file=file)
