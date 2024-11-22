import zlib
import hashlib
input_string = "Exemplo de string para hash"
# Convertendo a string para bytes, 
# pois os métodos de hash precisam de dados binários
input_bytes = input_string.encode('utf-8')
checksum = sum(input_bytes)
crc32 = zlib.crc32(input_bytes)
md5_hash = hashlib.md5(input_bytes).hexdigest()
sha1_hash = hashlib.sha1(input_bytes).hexdigest()
sha256_hash = hashlib.sha256(input_bytes).hexdigest()
print("String de entrada:", input_string)
print("Checksum:", checksum)
print("crc32:", format(crc32, '08x'))
print("MD5:", md5_hash)
print("SHA-1:", sha1_hash)
print("SHA-256:", sha256_hash)