import bz2

# Comprimir
with bz2.BZ2File('arquivo.txt.bz2', 'w') as f:
    f.write(b"Conteudo do arquivo")

# Descompactar
with bz2.BZ2File('arquivo.txt.bz2', 'r') as f:
    print(f.read())
