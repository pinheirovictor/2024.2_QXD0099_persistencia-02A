# Carrega todas as abas como um dicionário de DataFrames
dfs = pd.read_excel('nome_do_arquivo.xlsx', sheet_name=None)

# Exibe as chaves do dicionário (nomes das planilhas)
print(dfs.keys())

# Exibe o DataFrame da primeira aba
print(dfs['Nome_da_Planilha'])
