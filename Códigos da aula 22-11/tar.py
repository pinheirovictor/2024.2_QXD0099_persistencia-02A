import tarfile

# Criar um TAR.GZ
with tarfile.open('arquivo.tar.gz', 'w:gz') as tar:
    tar.add('pasta/')

# Extrair
with tarfile.open('arquivo.tar.gz', 'r:gz') as tar:
    tar.extractall('pasta_destino')
