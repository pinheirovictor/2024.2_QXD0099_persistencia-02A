from bs4 import BeautifulSoup

with open("arquivo.xml", "r") as file:
    soup = BeautifulSoup(file, "xml")
for tag in soup.find_all("tag_name"):
    print(tag.text)
