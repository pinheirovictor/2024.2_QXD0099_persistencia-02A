# Abrindo o arquivo para leitura
with open('arquivo.txt', 'r', encoding='utf-8') as file:
    # Lê a primeira linha
    s = file.readline()

    # Enquanto houver linhas para ler
    while s:
        # Imprime a linha atual
        print(s.strip())  # .strip() remove os espaços em branco no final da linha, incluindo o \n
        # Lê a próxima linha
        s = file.readline()
