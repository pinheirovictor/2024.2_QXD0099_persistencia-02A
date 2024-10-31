# Criando um arquivo com BOM em UTF-8
content = "Este é um arquivo com BOM para UTF-8.\nOutra linha de exemplo."

# Abrindo o arquivo com 'utf-8-sig' para adicionar o BOM automaticamente
with open("arquivo_com_bom.txt", "w", encoding="utf-8-sig") as file:
    file.write(content)
