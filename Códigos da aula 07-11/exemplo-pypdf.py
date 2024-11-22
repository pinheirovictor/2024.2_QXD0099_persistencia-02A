from PyPDF2 import PdfReader

reader = PdfReader("./Relatorio_anual.pdf")
for page in reader.pages:
    print(page.extract_text())
