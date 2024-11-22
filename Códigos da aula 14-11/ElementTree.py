import xml.etree.ElementTree as ET

tree = ET.parse('arquivo.xml')
root = tree.getroot()
for elem in root:
    print(elem.tag, elem.attrib)
