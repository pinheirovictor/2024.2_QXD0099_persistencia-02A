# Abrindo o arquivo no modo binário para verificar os primeiros bytes manualmente
with open('arquivoBom.txt', 'rb') as file:
    primeiro_bytes = file.read(3)  # Lê os primeiros 3 bytes

    # Verifica se a BOM está presente
    if primeiro_bytes == b'\xef\xbb\xbf':
        print("BOM detectada no arquivo!")
        # Ler o restante do arquivo, agora sem a BOM
        conteudo = file.read().decode('utf-8')
    else:
        # Se não houver BOM, volta ao início e lê o arquivo inteiro
        file.seek(0)
        conteudo = file.read().decode('utf-8')

# Exibe o conteúdo do arquivo
print(conteudo)
