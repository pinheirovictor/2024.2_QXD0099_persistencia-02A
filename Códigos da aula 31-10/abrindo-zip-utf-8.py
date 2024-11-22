import zipfile

# Caminho do arquivo ZIP
zip_file_path = "./tb1.zip"

# Abre o arquivo ZIP
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    # Pega o nome do primeiro arquivo dentro do ZIP
    file_name = zip_ref.namelist()[0]
    
    # Abre o arquivo dentro do ZIP
    with zip_ref.open(file_name) as file:
        # Usa o scanner (como o Scanner no Java, lendo linha por linha)
        for line in file:
            print(line.decode('utf-8').strip())  # Converte bytes para string e remove quebras de linha
