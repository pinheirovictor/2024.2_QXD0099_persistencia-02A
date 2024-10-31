# Leitura da entrada do usuário (console)
import sys

# Lê a primeira linha da entrada padrão
s = sys.stdin.readline().strip()  # .strip() remove espaços em branco e nova linha

# Enquanto houver algo na entrada
while s:
    # Exibe a linha lida
    print(s)
    # Lê a próxima linha da entrada padrão
    s = sys.stdin.readline().strip()
