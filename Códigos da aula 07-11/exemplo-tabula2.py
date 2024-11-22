import tabula

# Caminho para o arquivo PDF
file_path = "./Relatorio_anual_dados.pdf"

# Extrai tabelas de todas as páginas e armazena como uma lista de DataFrames
tables = tabula.read_pdf(file_path, pages="all", multiple_tables=True)

# Exibe o conteúdo de cada tabela extraída
for i, table in enumerate(tables):
    print(f"Tabela {i+1}:")
    print(table)
    print("\n")
    
tabula.convert_into(file_path, "output.csv", output_format="csv", pages="all")
