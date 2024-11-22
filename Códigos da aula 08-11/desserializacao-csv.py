import csv

# Ler dados do arquivo CSV
with open("dados.csv", "r") as file:
    reader = csv.DictReader(file)
    dados = [row for row in reader]

print(dados)
