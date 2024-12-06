import hashlib

# Caminho para o arquivo a ser verificado
file_path = 'arquivo.txt'

# Gerar hash SHA-256
with open(file_path, 'rb') as f:
    file_data = f.read()
    sha256_hash = hashlib.sha256(file_data).hexdigest()

print(f"Hash SHA-256: {sha256_hash}")
