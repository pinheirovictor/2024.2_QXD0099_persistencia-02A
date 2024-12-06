import hashlib

# Caminhos dos arquivos
file_path = 'arquivo.txt'  # Arquivo a ser verificado
checksum_file_path = 'checksum.txt'  # Arquivo contendo o checksum esperado

# Função para calcular o checksum de um arquivo
def calculate_checksum(file_path, hash_algorithm='sha256'):
    try:
        # Seleciona o algoritmo de hash
        hash_function = hashlib.new(hash_algorithm)
        
        # Leitura do arquivo em blocos para eficiência
        with open(file_path, 'rb') as file:
            while chunk := file.read(8192):
                hash_function.update(chunk)
        
        return hash_function.hexdigest()
    except FileNotFoundError:
        print(f"Erro: O arquivo '{file_path}' não foi encontrado.")
        return None

# Função para ler o checksum esperado
def read_expected_checksum(checksum_file_path):
    try:
        with open(checksum_file_path, 'r') as checksum_file:
            return checksum_file.read().strip()
    except FileNotFoundError:
        print(f"Erro: O arquivo de checksum '{checksum_file_path}' não foi encontrado.")
        return None

# Função para salvar o checksum calculado em um arquivo
def save_checksum(checksum, checksum_file_path):
    try:
        with open(checksum_file_path, 'w') as checksum_file:
            checksum_file.write(checksum)
        print(f"Checksum salvo em '{checksum_file_path}'.")
    except Exception as e:
        print(f"Erro ao salvar o checksum: {e}")

# Calcular e comparar checksums
expected_checksum = read_expected_checksum(checksum_file_path)
calculated_checksum = calculate_checksum(file_path)

if calculated_checksum:
    print(f"Checksum Calculado: {calculated_checksum}")
    if expected_checksum:
        print(f"Checksum Esperado: {expected_checksum}")
        if calculated_checksum == expected_checksum:
            print("Integridade verificada: o arquivo é autêntico.")
        else:
            print("Integridade comprometida: o arquivo foi alterado ou corrompido.")
    else:
        print("Checksum esperado não encontrado. Salvando o checksum calculado como referência.")
        save_checksum(calculated_checksum, checksum_file_path)
