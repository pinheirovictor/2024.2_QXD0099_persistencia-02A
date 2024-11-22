from bs4 import BeautifulSoup
import requests

# Conexão com a página e extração do título
response = requests.get("https://quotes.toscrape.com/")
doc = BeautifulSoup(response.content, "html.parser")
title = doc.title.string

# Exemplo de impressão do título
print("Título:", title)

# # Leitura de arquivo HTML local
# with open("./input.html", encoding="utf-8") as file:
#     doc = BeautifulSoup(file, "html.parser")

# # Seleção de links e imagens com extensão .png
# links = doc.select("a[href]")
# pngs = doc.select("img[src$='.png']")

# # Seleção do primeiro elemento com a classe 'masthead'
# masthead = doc.select_one("div.masthead")

# # Seleção de links de resultados
# result_links = doc.select("h3.r > a")


