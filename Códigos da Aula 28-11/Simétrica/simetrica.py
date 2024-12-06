from cryptography.fernet import Fernet

# Gerar chave
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Encriptar arquivo
with open('arquivo.txt', 'rb') as file:
    data = file.read()
encrypted_data = cipher_suite.encrypt(data)

# Salvar arquivo encriptado
with open('arquivo_encrypted.txt', 'wb') as file:
    file.write(encrypted_data)

# Decriptar arquivo
with open('arquivo_encrypted.txt', 'rb') as file:
    encrypted_data = file.read()
decrypted_data = cipher_suite.decrypt(encrypted_data)

# Salvar arquivo decriptado
with open('arquivo_decrypted.txt', 'wb') as file:
    file.write(decrypted_data)
