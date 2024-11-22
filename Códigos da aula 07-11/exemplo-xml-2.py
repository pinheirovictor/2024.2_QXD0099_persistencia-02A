from bs4 import BeautifulSoup

with open("./dados.xml", "r") as file:
    soup = BeautifulSoup(file, "xml")  # o "xml" parser é específico para XML

# Buscando e extraindo dados
for elemento in soup.find_all("clientes"):
    valor = elemento.find("cliente").text
    print(valor)
