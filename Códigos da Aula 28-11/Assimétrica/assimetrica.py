from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization

# Gerar par de chaves
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()

# Salvar chave privada
with open("private_key.pem", "wb") as file:
    file.write(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ))

# Salvar chave pública
with open("public_key.pem", "wb") as file:
    file.write(public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ))

# Encriptar arquivo
with open('arquivo.txt', 'rb') as file:
    data = file.read()
encrypted_data = public_key.encrypt(
    data,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# Salvar arquivo encriptado
with open('arquivo_encrypted.txt', 'wb') as file:
    file.write(encrypted_data)

# Decriptar arquivo
with open('arquivo_encrypted.txt', 'rb') as file:
    encrypted_data = file.read()
decrypted_data = private_key.decrypt(
    encrypted_data,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# Salvar arquivo decriptado
with open('arquivo_decrypted.txt', 'wb') as file:
    file.write(decrypted_data)
