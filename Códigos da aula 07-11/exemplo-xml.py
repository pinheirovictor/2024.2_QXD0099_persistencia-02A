import xml.etree.ElementTree as ET

# Parse do arquivo XML
tree = ET.parse("./dados.xml")
root = tree.getroot()

# Acessando dados por tags
for cliente in root.findall("cliente"):
    nome = cliente.find("nome").text
    email = cliente.find("email").text
    telefone = cliente.find("telefone").text
    print(f"Nome: {nome}, Email: {email}, Telefone: {telefone}")

    # Acessando compras de cada cliente
    for compra in cliente.find("compras").findall("compra"):
        id_compra = compra.find("id_compra").text
        data = compra.find("data").text
        total = compra.find("total").text
        print(f"  Compra ID: {id_compra}, Data: {data}, Total: {total}")

        # Acessando itens de cada compra
        for item in compra.find("itens").findall("item"):
            produto = item.find("produto").text
            quantidade = item.find("quantidade").text
            preco_unitario = item.find("preco_unitario").text
            print(f"    Produto: {produto}, Quantidade: {quantidade}, Preço Unitário: {preco_unitario}")
