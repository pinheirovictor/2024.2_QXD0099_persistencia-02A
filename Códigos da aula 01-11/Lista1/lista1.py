import pandas as pd
import matplotlib.pyplot as plt

# Carregar o CSV para um DataFrame (caminho relativo)
df = pd.read_csv('vendas.csv')

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

# Criar um gráfico de barras para visualizar as vendas totais por produto
plt.figure(figsize=(10, 6))
total_vendas.plot(kind='bar')
plt.title('Total de Vendas por Produto')
plt.xlabel('Produto')
plt.ylabel('Total Vendido (R$)')
plt.tight_layout()
plt.savefig('total_vendas_produto.png')
plt.show()
