import tabula

# Extrai todas as tabelas de um PDF para uma lista de DataFrames
tables = tabula.read_pdf("./Relatorio_anual_dados.pdf", pages="all")

# Exibe a primeira tabela
print(tables[0])
