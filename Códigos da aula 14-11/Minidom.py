from xml.dom import minidom

doc = minidom.parse("arquivo.xml")
root = doc.documentElement
print(root.tagName)
