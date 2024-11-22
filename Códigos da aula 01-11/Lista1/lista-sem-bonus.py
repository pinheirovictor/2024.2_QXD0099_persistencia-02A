import pandas as pd

# Carregar o CSV para um DataFrame
df = pd.read_csv('vendas_grande.csv')

# Calcular o total de vendas por produto
df['Total_Venda'] = df['Quantidade'] * df['Preco_Unitario']
total_vendas = df.groupby('Produto')['Total_Venda'].sum()

# Filtrar vendas de janeiro de 2023
df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y')
vendas_janeiro = df[(df['Data'].dt.month == 1) & (df['Data'].dt.year == 2023)]

# Salvar o DataFrame filtrado em um novo arquivo CSV
vendas_janeiro.to_csv('vendas_janeiro.csv', index=False)

# Salvar o total de vendas por produto em uma planilha Excel com cada produto em uma aba
with pd.ExcelWriter('total_vendas_produto.xlsx') as writer:
    for produto, dados in df.groupby('Produto'):
        dados.to_excel(writer, sheet_name=produto, index=False)

