from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.padding import PSS, MGF1
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import (
    load_pem_private_key,
    Encoding,
    PrivateFormat,
    PublicFormat,
    NoEncryption,
)
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import datetime
import os

app = FastAPI()

# Caminhos para salvar as chaves e imagem
PRIVATE_KEY_PATH = "private_key.pem"
PUBLIC_KEY_PATH = "public_key.pem"
SIGNATURE_IMAGE_PATH = "signature_image.png"  # Caminho para a imagem da assinatura

def generate_keys():
    """
    Gera um par de chaves RSA e salva em arquivos PEM se não existirem.
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    private_key_pem = private_key.private_bytes(
        encoding=Encoding.PEM,
        format=PrivateFormat.PKCS8,
        encryption_algorithm=NoEncryption(),
    )
    public_key = private_key.public_key()
    public_key_pem = public_key.public_bytes(
        encoding=Encoding.PEM,
        format=PublicFormat.SubjectPublicKeyInfo,
    )

    # Salvar as chaves em arquivos
    with open(PRIVATE_KEY_PATH, "wb") as f:
        f.write(private_key_pem)
    with open(PUBLIC_KEY_PATH, "wb") as f:
        f.write(public_key_pem)

# Gerar as chaves caso ainda não existam
if not os.path.exists(PRIVATE_KEY_PATH) or not os.path.exists(PUBLIC_KEY_PATH):
    generate_keys()

# Carregar a chave privada para assinatura
with open(PRIVATE_KEY_PATH, "rb") as key_file:
    private_key = load_pem_private_key(key_file.read(), password=None)

def add_signatures_page(writer: PdfWriter, signatures: list, image_path: str):
    """
    Adiciona uma única página com todas as assinaturas ao final do PDF.
    """
    # Caminho temporário para o PDF da página de assinaturas
    temp_page_path = "temp_signatures_page.pdf"

    # Configurações da página em branco
    c = canvas.Canvas(temp_page_path, pagesize=letter)
    width, height = letter

    # Cabeçalho da página de assinaturas
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Relatório de Assinaturas")

    # Configurar posição inicial abaixo do cabeçalho
    y_position = height - 100  # Posição inicial na página

    c.setFont("Helvetica", 12)
    for signature in signatures:
        if y_position < 100:  # Verifica se o espaço acabou na página
            c.showPage()  # Cria uma nova página se necessário
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, height - 50, "Assinaturas (continuação)")
            y_position = height - 100  # Reinicia a posição na nova página
            c.setFont("Helvetica", 12)

        # Adicionar imagem da assinatura
        if os.path.exists(image_path):
            c.drawImage(image_path, 50, y_position - 20, width=50, height=50)  # Imagem 50x50px
            text_x_start = 110  # Texto começa ao lado da imagem
        else:
            text_x_start = 50  # Se não houver imagem, o texto começa mais à esquerda

        # Adicionar texto ao lado da imagem
        text_y_position = y_position + 20  # Alinha o texto ao topo da imagem
        for line in signature.split("\n"):
            c.drawString(text_x_start, text_y_position, line)
            text_y_position -= 15  # Move para a próxima linha do texto

        y_position -= 70  # Move a posição para a próxima assinatura

    c.save()

    # Ler a página criada e adicioná-la ao PDF original
    temp_reader = PdfReader(temp_page_path)
    for page in temp_reader.pages:
        writer.add_page(page)

    # Remover o arquivo temporário
    os.remove(temp_page_path)


@app.post("/sign-pdf/")
async def sign_pdf(file: UploadFile = File(...)):
    """
    Endpoint que recebe um arquivo PDF, o assina digitalmente e retorna o PDF assinado.
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="O arquivo enviado deve ser um PDF.")

    # Salvar o PDF enviado pelo cliente
    input_pdf_path = f"input_{file.filename}"
    with open(input_pdf_path, "wb") as f:
        f.write(await file.read())

    try:
        # Ler o conteúdo do PDF
        reader = PdfReader(input_pdf_path)
        writer = PdfWriter()

        # Copiar todas as páginas do PDF original para o novo PDF
        for page in reader.pages:
            writer.add_page(page)

        # Criar assinatura
        data_to_sign = b"".join([page.extract_text().encode() for page in reader.pages])
        signature = private_key.sign(
            data=data_to_sign,
            padding=padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            algorithm=hashes.SHA256(),
        )
        signature_hash = signature.hex()

        # Informações da assinatura
        signer_name = "Francisco Victor da Silva Pinheiro"
        timestamp = datetime.datetime.now().strftime("%H:%M:%S de %d/%m/%Y")
        signature_text = (
            f"Documento assinado eletronicamente por {signer_name}\n"
            f"às {timestamp} conforme horário oficial de Brasília.\n"
            f"{signature_hash[:32]}"  # Trunca o hash para 32 caracteres
        )

        # Adicionar a página de assinaturas ao final do PDF
        add_signatures_page(writer, [signature_text], SIGNATURE_IMAGE_PATH)

        # Salvar o PDF assinado
        signed_pdf_path = f"signed_{file.filename}"
        with open(signed_pdf_path, "wb") as f:
            writer.write(f)

        # Retornar PDF assinado como resposta
        return FileResponse(
            signed_pdf_path, media_type="application/pdf", filename=signed_pdf_path
        )
    finally:
        # Limpar arquivos temporários
        if os.path.exists(input_pdf_path):
            os.remove(input_pdf_path)

@app.post("/verify-signature/")
async def verify_signature(file: UploadFile = File(...)):
    """
    Endpoint que recebe um PDF assinado e verifica se a assinatura é válida usando RSA.
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="O arquivo enviado deve ser um PDF.")

    # Salvar o PDF enviado pelo cliente
    signed_pdf_path = f"uploaded_{file.filename}"
    with open(signed_pdf_path, "wb") as f:
        f.write(await file.read())

    print("PDF recebido e salvo localmente.")

    try:
        # Ler o PDF enviado
        reader = PdfReader(signed_pdf_path)
        print("PDF lido com sucesso.")

        # Extrair o texto da última página
        signature_page = reader.pages[-1]
        signature_text = signature_page.extract_text()
        print("Texto extraído da última página:", signature_text)

        # Extração da assinatura RSA (última linha)
        try:
            lines = signature_text.split("\n")
            signature_hex = lines[-1].strip()  # Última linha contém a assinatura em hex
            signature_bytes = bytes.fromhex(signature_hex)  # Converter assinatura para bytes
            print("Assinatura extraída com sucesso (hex):", signature_hex)

        except Exception as e:
            print("Erro ao extrair a assinatura:", str(e))
            raise HTTPException(status_code=400, detail=f"Erro ao extrair a assinatura: {str(e)}")

        # Carregar a chave pública
        with open(PUBLIC_KEY_PATH, "rb") as f:
            public_key = load_pem_public_key(f.read())
        print("Chave pública carregada com sucesso.")

        # Recalcular os dados originais para verificação (todas as páginas exceto a última)
        original_data = b"".join(
            page.extract_text().encode("utf-8", errors="ignore") for page in reader.pages[:-1]
        )
        print("Dados originais para verificação:", original_data.decode("utf-8", errors="ignore"))

        # Verificar a assinatura
        try:
            public_key.verify(
                signature_bytes,  # Assinatura extraída
                original_data,  # Dados originais do PDF
                PSS(
                    mgf=MGF1(hashes.SHA256()),
                    salt_length=PSS.MAX_LENGTH,
                ),
                hashes.SHA256(),
            )
            print("Assinatura verificada com sucesso!")
        except Exception as e:
            print("Erro na verificação da assinatura:", str(e))
            raise HTTPException(
                status_code=400, detail=f"A assinatura não é válida ou foi alterada: {str(e)}"
            )

        return {"detail": "A assinatura é válida e o documento não foi alterado."}

    except Exception as e:
        print("Erro geral:", str(e))
        raise HTTPException(
            status_code=400, detail=f"Erro na verificação da assinatura: {str(e)}"
        )
    finally:
        # Limpar arquivos temporários
        if os.path.exists(signed_pdf_path):
            os.remove(signed_pdf_path)
            print("Arquivo temporário removido.")