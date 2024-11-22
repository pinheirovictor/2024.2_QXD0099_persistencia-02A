import os
from zipfile import ZipFile

# Caminho da pasta com arquivos de texto
diretorio = "./textos"
# Nome do arquivo consolidado
consolidado = "consolidado.txt"
# Nome do arquivo ZIP final
zip_final = "saida.zip"

# Etapa 1: Processar arquivos
resultados = []
for nome_arquivo in os.listdir(diretorio):
    caminho_arquivo = os.path.join(diretorio, nome_arquivo)
    
    if nome_arquivo.endswith(".txt") and os.path.isfile(caminho_arquivo):
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.readlines()

            # Remover linhas em branco e calcular estatísticas
            conteudo_filtrado = [linha.strip() for linha in conteudo if linha.strip()]
            num_palavras = sum(len(linha.split()) for linha in conteudo_filtrado)
            num_caracteres = sum(len(linha) for linha in conteudo_filtrado)

            # Salvar as estatísticas no resultado
            resultados.append(f"{nome_arquivo} - Palavras: {num_palavras}, Caracteres: {num_caracteres}")

# Etapa 2: Escrever no arquivo consolidado
with open(consolidado, "w", encoding="utf-8") as arquivo_saida:
    for resultado in resultados:
        arquivo_saida.write(resultado + "\n")

# Etapa 3: Compactar em um arquivo ZIP
with ZipFile(zip_final, "w") as zip_arquivo:
    zip_arquivo.write(consolidado)

print(f"Processamento completo! Resultados salvos em '{consolidado}' e compactados em '{zip_final}'.")
