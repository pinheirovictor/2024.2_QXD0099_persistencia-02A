import socket
import person_pb2

def create_person():
    person = person_pb2.Person()
    person.name = "Bob"
    person.id = 5678  # Este campo precisa ser atribuído corretamente
    person.email = "bob@example.com"
    return person.SerializeToString()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 5000))
server.listen(1)
print("Servidor aguardando conexão...")

conn, addr = server.accept()
print(f"Conexão de {addr}")

data = create_person()
conn.sendall(data)
conn.close()
