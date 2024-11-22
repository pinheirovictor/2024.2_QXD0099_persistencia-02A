from pdfminer.high_level import extract_text

text = extract_text("./Relatorio_anual.pdf")
print(text)
