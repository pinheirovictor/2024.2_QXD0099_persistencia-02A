import zipfile

# Caminho do arquivo ZIP
zip_file_path = "./tb1.zip"

# Abre o arquivo ZIP para leitura
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    # Lista os arquivos dentro do ZIP
    for file_name in zip_ref.namelist():
        # Abre o arquivo dentro do ZIP
        with zip_ref.open(file_name) as file:
            # Lê o conteúdo do arquivo
            for line in file:
                # Converte de bytes para string e remove quebras de linha
                print(line.decode('utf-8').strip())
