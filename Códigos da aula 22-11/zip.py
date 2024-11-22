import zipfile

# Criar um arquivo ZIP
with zipfile.ZipFile('arquivo.zip', 'w') as zipf:
    zipf.write('arquivo1.txt')  # Substitua pelo caminho do arquivo
    zipf.write('arquivo2.txt')

# Extrair um arquivo ZIP
with zipfile.ZipFile('arquivo.zip', 'r') as zipf:
    zipf.extractall('pasta_destino')  # Substitua pelo caminho da pasta de destino
