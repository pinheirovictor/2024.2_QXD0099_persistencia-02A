# Abrindo o arquivo para escrita
with open('arquivoTeste.txt', 'w', encoding='utf-8') as file:
    # Lendo strings do teclado
    while True:
        try:
            # Lê uma linha do teclado
            line = input()
            # Escreve a linha no arquivo
            print(line, file=file)
        except EOFError:
            # Termina o loop quando não houver mais entrada (Ctrl+D no Linux/macOS ou Ctrl+Z no Windows)
            break
