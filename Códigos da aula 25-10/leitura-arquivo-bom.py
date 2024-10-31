# Abrindo o arquivo que pode conter uma BOM, utilizando 'utf-8-sig' para lidar com a BOM automaticamente
with open('arquivo_com_bom.txt', 'r', encoding='utf-8-sig') as file:
    conteudo = file.read()

# Exibe o conteúdo do arquivo, sem a BOM
print(conteudo)
