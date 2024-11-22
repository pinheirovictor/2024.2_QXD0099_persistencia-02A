from lxml import etree

tree = etree.parse('arquivo.xml')
root = tree.getroot()
for element in root:
    print(element.tag, element.text)
