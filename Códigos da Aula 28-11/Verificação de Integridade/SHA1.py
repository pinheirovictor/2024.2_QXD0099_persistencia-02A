import hashlib

# Caminho para o arquivo a ser verificado
file_path = 'arquivo.txt'

# Gerar hash SHA-1
with open(file_path, 'rb') as f:
    file_data = f.read()
    sha1_hash = hashlib.sha1(file_data).hexdigest()

print(f"Hash SHA-1: {sha1_hash}")
