import hashlib

# Caminho para o arquivo a ser verificado
file_path = 'md5.txt'

# Hash MD5 esperado (gerado anteriormente e armazenado)
expected_md5_hash = '8e506a437730815e2574c35dcadfccbe'

# Gerar o hash MD5 do arquivo atual
def calculate_md5(file_path):
    with open(file_path, 'rb') as f:
        file_data = f.read()
        return hashlib.md5(file_data).hexdigest()

# Comparar o hash calculado com o esperado
calculated_md5_hash = calculate_md5(file_path)
print(f"Hash MD5 Calculado: {calculated_md5_hash}")
print(f"Hash MD5 Esperado: {expected_md5_hash}")

if calculated_md5_hash == expected_md5_hash:
    print("Integridade verificada: o arquivo é autêntico.")
else:
    print("Integridade comprometida: o arquivo foi alterado ou corrompido.")
