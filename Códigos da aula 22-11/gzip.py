import gzip

# Comprimir um arquivo
with open('arquivo.txt', 'rb') as f_in:
    with gzip.open('arquivo.txt.gz', 'wb') as f_out:
        f_out.writelines(f_in)

# Descomprimir um arquivo
with gzip.open('arquivo.txt.gz', 'rb') as f_in:
    with open('arquivo_descomprimido.txt', 'wb') as f_out:
        f_out.writelines(f_in)
