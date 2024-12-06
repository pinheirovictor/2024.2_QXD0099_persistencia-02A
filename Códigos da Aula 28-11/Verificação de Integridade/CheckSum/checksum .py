import hashlib

# Caminho dos arquivos
file_path = 'arquivo.txt'
checksum_file_path = 'checksum.txt'

# Função para calcular o checksum usando hashlib (SHA-256 por padrão)
def calculate_checksum(file_path, hash_algorithm='sha256'):
    try:
        hash_function = hashlib.new(hash_algorithm)
        with open(file_path, 'rb') as file:
            while chunk := file.read(8192):
                hash_function.update(chunk)
        return hash_function.hexdigest()
    except FileNotFoundError:
        print(f"Erro: O arquivo '{file_path}' não foi encontrado.")
        return None

# Calcular o checksum e salvar no arquivo
checksum_value = calculate_checksum(file_path)
if checksum_value:
    with open(checksum_file_path, 'w') as checksum_file:
        checksum_file.write(checksum_value)
    print(f"Checksum salvo em '{checksum_file_path}'.")
