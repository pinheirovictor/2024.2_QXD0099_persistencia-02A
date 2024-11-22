import xmltodict

with open("arquivo.xml") as file:
    data = xmltodict.parse(file.read())
print(data['root']['tag_name'])
