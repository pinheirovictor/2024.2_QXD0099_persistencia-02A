import os
import rarfile

# Comprimir com RAR (requer instalação do programa RAR)
os.system('rar a arquivo.rar arquivo1.txt arquivo2.txt')  # Substitua pelos arquivos

# Descompactar um arquivo RAR
with rarfile.RarFile('arquivo.rar') as rar:
    rar.extractall('pasta_destino')  # Substitua pelo caminho da pasta de destino
