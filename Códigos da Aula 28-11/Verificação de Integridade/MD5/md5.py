import hashlib

# Caminho para o arquivo a ser verificado
file_path = 'md5.txt'

# Gerar hash MD5
with open(file_path, 'rb') as f:
    file_data = f.read()
    md5_hash = hashlib.md5(file_data).hexdigest()

with open("md5_hash.txt", "a") as file:
    print(md5_hash, file=file)
    
print(f"Hash MD5: {md5_hash}")
